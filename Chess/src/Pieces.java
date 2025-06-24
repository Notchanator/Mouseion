import processing.core.PImage;
import java.awt.*;
import java.awt.geom.Point2D;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public abstract class Pieces {

    protected Point2D.Float position;
    protected List<PImage> image;
    protected String color;
    protected Set<Point2D.Float> moves;
    protected boolean firstPiece;
    protected int imageIndex = 0;

    public Pieces(Point2D.Float position, List<PImage> image, String color) {
        this.position = position;
        this.image = image;
        this.color = color;
    }

    public Point2D.Float getPosition() { return this.position; }

    public List<PImage> getImage() { return this.image;}

    public String getColor() { return this.color;}

    public void setPosition(Point2D.Float newPos) { this.position = newPos;}

    public int getImageIndex() {return this.imageIndex;}

    public void setImageIndex(){
        this.imageIndex = (this.imageIndex + 1) % 2;
    }

    public abstract Set<Point2D.Float> getMoves(Board board);

    public void validMoves(Board board, int pos1, int pos2, int len){
        firstPiece = false;
        for (int i = 1; i < len; i++) {
            Point2D.Float newPos = new Point2D.Float(position.x + (pos1 * i), position.y + (pos2 * i));
            if (board.isOccupied(newPos) && board.getOccupancyCell(newPos).color.equals(this.color)) break;
            if (firstPiece) break;
            if (board.isOccupied(newPos) && !board.getOccupancyCell(newPos).color.equals(this.color)) firstPiece = true;
            moves.add(newPos);
        }
    }

}
