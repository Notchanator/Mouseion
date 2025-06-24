import java.awt.*;
import java.util.Arrays;
import java.util.List;

public class Parse {

    private String[] properties;
    private Images images;
    private WorldModel world;

    private final int NUM_PROPERTIES = 5;
    private final int RED_NUM_PROPERTIES = 3;

    private final String RED_KEY = "RedCar";
    private final int RED_COL = 1;
    private final int RED_ROW = 2;

    private final List<String> TWO_KEY = Arrays.asList("TwoCarHor", "TwoCarVert");
    private final int TWO_ID = 1;
    private final int TWO_COL = 2;
    private final int TWO_ROW = 3;
    private final int TWO_DIRECTION = 4;

    private final List<String> THREE_KEY = Arrays.asList("ThreeCarHor", "ThreeCarVert");
    private final int THREE_ID = 1;
    private final int THREE_COL = 2;
    private final int THREE_ROW = 3;
    private final int THREE_DIRECTION = 4;

    public Parse(String[] line, Images images, WorldModel world){
        this.properties = line;
        this.images = images;
        this.world = world;
    }

    public boolean redCar(){
        if (properties.length == RED_NUM_PROPERTIES) {
            Point pos = new Point(Integer.parseInt(properties[RED_COL]), Integer.parseInt(properties[RED_ROW]));
            Cars car = new RedCar(pos, images.getImageList(RED_KEY));
            world.tryAddCar(car);
        }
        return properties.length == RED_NUM_PROPERTIES;
    }

    public boolean twoCar(int indx){
        if (properties.length == NUM_PROPERTIES) {
            Point pos = new Point(Integer.parseInt(properties[TWO_COL]), Integer.parseInt(properties[TWO_ROW]));
            Cars car = new TwoCar(properties[TWO_ID], pos, images.getImageList(TWO_KEY.get(indx)),
                    Boolean.parseBoolean(properties[TWO_DIRECTION]));
            world.tryAddCar(car);
        }
        return properties.length == NUM_PROPERTIES;
    }

    public boolean threeCar(int indx){
        if (properties.length == NUM_PROPERTIES) {
            Point pos = new Point(Integer.parseInt(properties[THREE_COL]), Integer.parseInt(properties[THREE_ROW]));
            Cars car = new ThreeCar(properties[THREE_ID], pos, images.getImageList(THREE_KEY.get(indx)),
                    Boolean.parseBoolean(properties[THREE_DIRECTION]));
            world.tryAddCar(car);
        }
        return properties.length == NUM_PROPERTIES;
    }
}
