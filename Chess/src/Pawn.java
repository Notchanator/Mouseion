import processing.core.PImage;
import java.awt.*;
import java.awt.geom.Point2D;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Pawn extends Pieces{

    private Point2D.Float start;

    public Pawn(Point2D.Float position, List<PImage> image, String color){
        super(position, image, color);
        this.start = position;
    }

    public Set<Point2D.Float> getMoves(Board board) { //Make this faster
        moves = new HashSet<>();
        if (startPosition()){
            if (color == "white"){
                validMoves(board, 0, -1, 3);
            } else {
                validMoves(board, 0, 1, 3);
            }
        } else {
            if (color == "white") {
                validMoves(board, 0, -1,2);
            } else {
                validMoves(board, 0, 1, 2);
            }
        }
        return moves;
    }

    public boolean startPosition() {
        return start.equals(this.position);
    }
}
