from pathlib import Path

import geopandas as gpd
from shapely.geometry import box
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


from config import *

DATA_DIR = Path(__file__).parent / "data"

class Geography:

    def __init__(self):
        self.loadData()

    def _loadLayer(self, name):
        DATA_DIR.mkdir(exist_ok=True)
        cache = DATA_DIR / f"{name}.gpkg"
        if cache.exists():
            return gpd.read_file(cache)
        gdf = gpd.read_file(f"zip+{SOURCES[name]}")
        gdf.to_file(cache, driver="GPKG")
        return gdf

    def loadData(self):
        allStates = self._loadLayer("states")
        # Restrict to the US, as some State Names also exist Elsewhere (e.g. Montana, Bulgaria).
        self.allStatesLayer = allStates[allStates["admin"] == "United States of America"]
        self.oceanLayer = self._loadLayer("ocean")
        self.riverLayer = self._loadLayer("rivers")
        self.lakeLayer = self._loadLayer("lakes")

    def _getStateLayer(self, state):
        return self.allStatesLayer[self.allStatesLayer["name"] == state].copy()

    def clipLayerToState(self, state):
        # Get State Boundary.
        selectedStateLayer = self._getStateLayer(state)
        minx, miny, maxx, maxy = selectedStateLayer.total_bounds
        # Create GDF Clip for the Space of the State (PADDING is in Degrees, so use the Source CRS).
        clipShape = gpd.GeoDataFrame(
            geometry=[
                box(
                    minx - PADDING,
                    miny - PADDING,
                    maxx + PADDING,
                    maxy + PADDING
                )
            ],
            crs=self.allStatesLayer.crs
        )
        # Clip each Layer to State.
        self.stateOcean = gpd.clip(self.oceanLayer, clipShape)
        self.stateRiver = gpd.clip(self.riverLayer, clipShape)
        self.stateLake = gpd.clip(self.lakeLayer, clipShape)

    def _projectToCRS(self, projection, crs):
        return projection.to_crs(crs)

    def addRiverBuffer(self, state, bufferSize=50):
        stateCRS = STATE_CRS[state]
        # Project the River to the State CRS.
        riverStateProjection = self._projectToCRS(self.stateRiver, stateCRS)
        # Add the Extra Meters onto the Geo-Object.
        riverStateProjection["geometry"] = riverStateProjection.geometry.buffer(bufferSize)
        # Project Back from the State CRS. Kept Separate so the Plot still Shows the Centerlines.
        self.stateRiverBuffer = self._projectToCRS(riverStateProjection, self.stateRiver.crs)

    def unionWaterBoundaries(self, state):
        stateCRS = STATE_CRS[state]
        # Project the Layers to the State CRS.
        projectedStateOcean = self._projectToCRS(self.stateOcean, stateCRS)
        projectedStateRiver = self._projectToCRS(self.stateRiverBuffer, stateCRS)
        projectedStateLake = self._projectToCRS(self.stateLake, stateCRS)
        # Union the Geo-Objects Together (Repairing any Geometry Invalidated by Reprojection, e.g. Alaska).
        self.stateWater = gpd.GeoSeries(
            [
                projectedStateOcean.make_valid().union_all(),
                projectedStateRiver.make_valid().union_all(),
                projectedStateLake.make_valid().union_all()
            ],
            crs=stateCRS
        ).union_all()

    def calculateWaterStateOverlap(self, state, bufferSize=1000):
        if state not in STATE_CRS:
            raise ValueError(f"Invalid State Specified: {state}")
        stateCRS = STATE_CRS[state]
        # Clip Layers to State, Buffer the River, and Union the Waters.
        self.clipLayerToState(state)
        self.addRiverBuffer(state, bufferSize)
        self.unionWaterBoundaries(state)
        # Get the State Border as Lines in the State CRS for Metric Lengths.
        selectedStateLayer = self._getStateLayer(state)
        stateBoundary = self._projectToCRS(selectedStateLayer, stateCRS).geometry.boundary
        # Intersection of Water and States.
        stateBorderWater = stateBoundary.intersection(self.stateWater)
        stateLength = stateBoundary.length.sum()
        waterLength = stateBorderWater.length.sum()
        # Drop Empty Geometries and Project Back for Plotting.
        stateWaterBoundary = self._projectToCRS(
            stateBorderWater[~stateBorderWater.is_empty],
            self.allStatesLayer.crs
        )
        return {
            "stateWaterBoundary" : stateWaterBoundary,
            "stateLength" : stateLength,
            "waterLength" : waterLength,
            "percentOverlap" : waterLength / stateLength * 100
        }

    def plot(self, state, stateWaterOverlap):
        fig, ax = plt.subplots(figsize=(8, 10))
        fig.patch.set_facecolor("#F0F4F8")
        ax.set_facecolor("#F0F4F8")
        # Plot in the State CRS so States Crossing the Antimeridian (e.g. Alaska) Stay in One Piece.
        stateCRS = STATE_CRS[state]
        selectedStateLayer = self._projectToCRS(self._getStateLayer(state), stateCRS)
        minx, miny, maxx, maxy = selectedStateLayer.total_bounds
        # PADDING is in Degrees, so Pad by a Fraction of the State's Extent Instead.
        pad = PLOT_PADDING * max(maxx - minx, maxy - miny)
        # Add Visual Layers (Skipping Empty Ones, e.g. Ocean for Landlocked States, to Avoid Geopandas Warnings).
        layers = [
            (self._projectToCRS(self.stateOcean, stateCRS), dict(color="#A8D5E2", linewidth=0)),
            (selectedStateLayer, dict(color="#EDE8D0", edgecolor="#B0A898", linewidth=0.6)),
            (self._projectToCRS(self.stateLake, stateCRS), dict(color="#A8D5E2", edgecolor="#6BAED6", linewidth=0.4)),
            (self._projectToCRS(self.stateRiver, stateCRS), dict(color="#6BAED6", linewidth=0.8)),
            (self._projectToCRS(stateWaterOverlap["stateWaterBoundary"], stateCRS), dict(color="#E63946", linewidth=2.2)),
        ]
        for layer, style in layers:
            if not layer.empty:
                layer.plot(ax=ax, **style)
        # Plot Config.
        ax.set_xlim(minx - pad, maxx + pad)
        ax.set_ylim(miny - pad, maxy + pad)
        ax.set_aspect("equal")
        ax.set_axis_off()
        ax.set_title(
            f"{state} Border — Water-Defined Segments\n"
            f"{stateWaterOverlap["percentOverlap"]:.1f}% water · "
            f"{stateWaterOverlap["waterLength"]/1000:,.0f} km / {stateWaterOverlap["stateLength"]/1000:,.0f} km total",
            fontsize=13, fontweight="bold", color="#2C3E50", pad=12,
        )

        legend_items = [
            mpatches.Patch(color="#A8D5E2", label="Ocean / Lakes"),
            mpatches.Patch(color="#6BAED6", label="Rivers"),
            mpatches.Patch(color="#EDE8D0", label=f"{state}"),
            mpatches.Patch(color="#E63946", label=f"Water border"),
        ]
        ax.legend(handles=legend_items, loc="lower left", frameon=True,
                framealpha=0.9, fontsize=9, edgecolor="#CCCCCC")

        plt.tight_layout()
        plt.show()
