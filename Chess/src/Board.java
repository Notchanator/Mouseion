import processing.core.PApplet;

import java.awt.*;
import java.awt.geom.Point2D;
import java.util.*;

public class Board {

    private int numRows;
    private int numCols;
    private Images images;
    private Pieces occupancy[][];
    public Set<Pieces> pieces;
    public String turn;


    private final float TILE_WIDTH = 80f;
    private final float TILE_HEIGHT = 80f;

    private final char PAWN = 'p';
    private final char ROOK = 'r';
    private final char KNIGHT = 'n';
    private final char BISHOP = 'b';
    private final char KING = 'k';
    private final char QUEEN = 'q';
    private final String WHITE_MOVE_KEY = "WhiteMove";
    private final String BLACK_MOVE_KEY = "BlackMove";

    public Board(int numRows, int numCols, Images images){
        this.numRows = numRows;
        this.numCols = numCols;
        this.occupancy = new Pieces[numRows][numCols];
        this.images = images;
        this.pieces = new HashSet<>();
        this.turn = "white";
    }


    public void readFEN(String FEN, Images images) {
        String[] ranks = FEN.split("/");
        Loading loader = new Loading(images, this);
        for (int i=0; i < ranks.length; i++){
            String rank = ranks[i];
            for (int j=0; j < rank.length(); j++){
                switch (Character.toLowerCase(rank.charAt(j)))
                {
                    case PAWN:
                        if (Character.isUpperCase(rank.charAt(i))) loader.createPawn(j,i,"white",0);
                        else loader.createPawn(j,i,"black",1);
                        break;
                    case ROOK:
                        if (Character.isUpperCase(rank.charAt(i))) loader.createRook(j,i,"white",0);
                        else loader.createRook(j,i,"black",1);
                        break;
                    case KNIGHT:
                        if (Character.isUpperCase(rank.charAt(i))) loader.createKnight(j,i,"white",0);
                        else loader.createKnight(j,i,"black",1);
                        break;
                    case BISHOP:
                        if (Character.isUpperCase(rank.charAt(i))) loader.createBishop(j,i,"white",0);
                        else loader.createBishop(j,i,"black",1);
                        break;
                    case KING:
                        if (Character.isUpperCase(rank.charAt(i))) loader.createKing(j,i,"white",0);
                        else loader.createKing(j,i,"black",1);
                        break;
                    case QUEEN:
                        if (Character.isUpperCase(rank.charAt(i))) loader.createQueen(j,i,"white",0);
                        else loader.createQueen(j,i,"black",1);
                        break;
                }
            }
        }
    }

    public void tryAddPiece(Pieces piece) {
            if (this.isOccupied(piece.getPosition()))
            {
                throw new IllegalArgumentException("position occupied");
            }

            this.addPiece(piece);
    }

    public boolean isOccupied(Point2D.Float pos)
    {
        return this.pointWithinBounds(pos) && this.getOccupancyCell(pos) != null;
    }

    public boolean pointWithinBounds(Point2D.Float pos){
        return pos.y >= 0 && pos.y < this.numRows && pos.x >= 0 && pos.x < this.numCols;
    }

    protected Pieces getOccupancyCell(Point2D.Float pos) {return this.occupancy[(int) pos.y][(int) pos.x];}

    protected void setOccupancyCell(Point2D.Float pos, Pieces piece){
        this.occupancy[(int) pos.y][(int) pos.x] = piece;
    }

    public void addPiece(Pieces piece){
        this.setOccupancyCell(piece.getPosition(), piece);
        this.pieces.add(piece);
    }

    public void drawBoard(PApplet screen){
        for (Pieces piece: pieces) {
            screen.image(piece.getImage().get(piece.getImageIndex()), piece.getPosition().x * TILE_WIDTH, piece.getPosition().y * TILE_HEIGHT );
        }
    }

    public void drawMoves(PApplet screen, Set<Point2D.Float> moves, Pieces piece) {
        if (piece.getColor() == "black") {
            for (Point2D.Float move : moves) {
                screen.image(images.getImageList(BLACK_MOVE_KEY).get(0), move.x * TILE_WIDTH, move.y * TILE_HEIGHT);
            }
        } else {
            for (Point2D.Float move : moves) {
                screen.image(images.getImageList(WHITE_MOVE_KEY).get(0), move.x * TILE_WIDTH, move.y * TILE_HEIGHT);
            }
        }
    }

    public boolean possibleMove(Set<Point2D.Float> moves, Point2D.Float move){
        return moves.contains(move);
    }

    public void deletePiece(Pieces piece){
        pieces.remove(piece);
    }

    public boolean checkmate(Pieces piece, Set<Point2D.Float> moves){
        for (Point2D.Float move: moves){
            if(isOccupied(move) && getOccupancyCell(move).getClass().equals(King.class)) {
                getOccupancyCell(move).setImageIndex();
                return true;
            }
        }
        return false;
    }

}
