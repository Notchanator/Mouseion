import processing.core.PApplet;
import processing.core.PImage;
import java.awt.*;
import java.awt.geom.Point2D;
import java.util.Arrays;
import java.util.List;


public class Loading {

    private Images images;
    private Board board;

    private final List<String> PAWN_KEY = Arrays.asList("WhitePawn", "BlackPawn");
    private final List<String> ROOK_KEY = Arrays.asList("WhiteRook", "BlackRook");
    private final List<String> KNIGHT_KEY = Arrays.asList("WhiteKnight", "BlackKnight");
    private final List<String> BISHOP_KEY = Arrays.asList("WhiteBishop", "BlackBishop");
    private final List<String> KING_KEY = Arrays.asList("WhiteKing", "BlackKing");
    private final List<String> QUEEN_KEY = Arrays.asList("WhiteQueen", "BlackQueen");

    public Loading (Images images, Board board) {
        this.images = images;
        this.board = board;
    }

    public void createRook(int row, int col, String color, int indx) {
        Point2D.Float pos = new Point2D.Float(row, col);
        Pieces rook = new Rook(pos, images.getImageList(ROOK_KEY.get(indx)) , color);
        this.board.tryAddPiece(rook);
    }

    public void createKnight(int row, int col, String color, int indx) {
        Point2D.Float pos = new Point2D.Float(row, col);
        Pieces knight = new Knight(pos, images.getImageList(KNIGHT_KEY.get(indx)) , color);
        this.board.tryAddPiece(knight);
    }

    public void createPawn(int row, int col, String color, int indx) {
        Point2D.Float pos = new Point2D.Float(row, col);
        Pieces pawn = new Pawn(pos, images.getImageList(PAWN_KEY.get(indx)) , color);
        this.board.tryAddPiece(pawn);
    }

    public void createBishop(int row, int col, String color, int indx) {
        Point2D.Float pos = new Point2D.Float(row, col);
        Pieces bishop = new Bishop(pos, images.getImageList(BISHOP_KEY.get(indx)) , color);
        this.board.tryAddPiece(bishop);
    }

    public void createKing(int row, int col, String color, int indx) {
        Point2D.Float pos = new Point2D.Float(row, col);
        Pieces king = new King(pos, images.getImageList(KING_KEY.get(indx)) , color);
        this.board.tryAddPiece(king);
    }

    public void createQueen(int row, int col, String color, int indx) {
        Point2D.Float pos = new Point2D.Float(row, col);
        Pieces queen = new Queen(pos, images.getImageList(QUEEN_KEY.get(indx)) , color);
        this.board.tryAddPiece(queen);
    }
}
