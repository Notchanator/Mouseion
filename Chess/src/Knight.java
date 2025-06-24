import processing.core.PImage;
import java.awt.*;
import java.awt.geom.Point2D;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Knight extends Pieces {

    public Knight(Point2D.Float position, List<PImage> image, String color) {
        super(position, image, color);
    }

    public Set<Point2D.Float> getMoves(Board board) { //Make this faster
        moves = new HashSet<>();
        validMoves(board, 2, 1,0);
        validMoves(board, 2, -1, 0);
        validMoves(board, -2, 1, 0);
        validMoves(board, -2, -1, 0);
        validMoves(board, 1, 2, 0);
        validMoves(board, 1, -2,0);
        validMoves(board, -1, 2, 0);
        validMoves(board, -1, -2 ,0);
        return moves;
    }

    @Override
    public void validMoves(Board board, int pos1, int pos2, int len){
        Point2D.Float newPos = new Point2D.Float(position.x + pos1, position.y + pos2);
        if (!board.isOccupied(newPos))
            moves.add(newPos);
        else if (!board.getOccupancyCell(newPos).getColor().equals(this.color))
            moves.add(newPos);

    }

}
