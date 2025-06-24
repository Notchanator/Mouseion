import processing.core.*;

import java.awt.*;
import java.awt.geom.Point2D;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.Set;

// Finish Checkmate: Make sure possible moves aren't in checkmate, change piece image
// Pawn can only attack on diagonal, need to factor in

public class VirtualWorld extends PApplet {

    private final float TILE_WIDTH = 80f;
    private final float TILE_HEIGHT = 80f;

    private final int numRows = 8;
    private final int numCols = 8;

    private PImage backgroundImage;
    private Board board;
    private Images images;

    private final String IMAGE_LIST_FILE_NAME = "imagelist";
    private final String BASE_BOARD = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR";

    private Pieces curPiece;
    private Point2D.Float curMouse;
    private Point2D.Float curPieceOldPos;
    private Set<Point2D.Float> possibleMoves;
    private boolean locked;
    private boolean checked = false;


    public void setup(){
        this.images = new Images(createImageColored(80, 80, 0xC4644F));
        loadImages(IMAGE_LIST_FILE_NAME, images, this);
        this.board = new Board(numRows, numCols, images);
        loadBoard(BASE_BOARD, images, this);
        this.backgroundImage = loadImage("/Users/notch/Desktop/Nathan Johnson/Projects/Chess/images/ChessBoard.png", "png");
        surface.setTitle("Chess Board");
    }

    public void draw() {
        if (this.board.turn == "white") this.background(255);
        else this.background(0);
        this.image(this.backgroundImage, 0, 0);
        this.board.drawBoard(this);
        if (locked && curPiece.color.equals(this.board.turn)){
            this.board.drawMoves(this, possibleMoves, curPiece);
        }
    }

    public void mousePressed(){
        curMouse = new Point2D.Float(mouseX/TILE_WIDTH, mouseY/TILE_HEIGHT);
        if (this.board.isOccupied(curMouse)){
            curPiece = this.board.getOccupancyCell(curMouse);
            curPieceOldPos = curPiece.getPosition();
            if (!checked || curPiece.getClass().equals(King.class)) {
                possibleMoves = curPiece.getMoves(this.board);
                locked = true;
            }
        } else {locked = false;}
    }

    public void mouseDragged(){
        if (locked && curPiece.color.equals(this.board.turn) &&
                (!checked || curPiece.getClass().equals(King.class))) {
            curPiece.setPosition(new Point2D.Float(curPiece.getPosition().x + mouseX/TILE_WIDTH - pmouseX/TILE_WIDTH,
                                                   curPiece.getPosition().y + mouseY/TILE_HEIGHT - pmouseY/TILE_HEIGHT));
            curMouse = new Point2D.Float(mouseX/TILE_WIDTH, mouseY/TILE_HEIGHT);

        }
    }

    public void mouseReleased(){
        Point2D.Float newPos = new Point2D.Float(Math.round(curPiece.getPosition().x), Math.round(curPiece.getPosition().y));
        if (this.board.possibleMove(possibleMoves, newPos)) {
            if (!curPiece.getPosition().equals(curPieceOldPos)) {
                curPiece.setPosition(newPos);
                if (board.isOccupied(curPiece.getPosition()) &&
                        !board.getOccupancyCell(curPiece.getPosition()).getColor().equals(curPiece.getColor())) {
                    this.board.deletePiece(board.getOccupancyCell(newPos));
                }
                this.board.setOccupancyCell(curPieceOldPos, null);
                this.board.setOccupancyCell(curPiece.getPosition(), curPiece);
                if (this.board.turn == "white") this.board.turn = "black";
                else this.board.turn = "white";
                checked = this.board.checkmate(curPiece, curPiece.getMoves(this.board));
                locked = false;
            }
        } else {
            curPiece.setPosition(curPieceOldPos);
        }
    }

    public void settings(){
        size(640,660);
    }

    public static void main(String[] args){
        PApplet.main(VirtualWorld.class);
    }

    public void loadImages(String filename, Images images, PApplet screen) {
        try {
            Scanner in = new Scanner(new File(filename));
            images.loadImages(in, screen);
        } catch (FileNotFoundException e) {
            System.err.println(e.getMessage());
        }
    }

    public void loadBoard(String FEN, Images images, PApplet screen) {
        this.board.readFEN(FEN, images);
    }


    public static PImage createImageColored(int width, int height, int color)
    // Delete at some point when no default textures are needed
    {
        PImage img = new PImage(width, height, RGB);
        img.loadPixels();
        for (int i = 0; i < img.pixels.length; i++)
        {
            img.pixels[i] = color;
        }
        img.updatePixels();
        return img;
    }

}
