import processing.core.PImage;
import java.awt.geom.Point2D;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Queen extends Pieces{

    public Queen(Point2D.Float position, List<PImage> image, String color){
        super(position, image, color);
    }

    public Set<Point2D.Float> getMoves(Board board) { //Make this faster
        moves = new HashSet<>();
        validMoves(board, 1, 0, 8);
        validMoves(board, 0, 1, 8);
        validMoves(board, -1, 0, 8);
        validMoves(board, 0, -1, 8);
        validMoves(board, 1, 1, 8);
        validMoves(board, -1, -1, 8);
        validMoves(board, 1, -1, 8);
        validMoves(board, -1, 1, 8);
        return moves;
    }

}
