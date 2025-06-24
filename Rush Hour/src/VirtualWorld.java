import java.awt.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import processing.core.*;

/*
 Make it so board names become integers for easier inputs
 Keeps track of completed boards
 Add restart screen
 Create random board generator
 Write algorithm that solves puzzles for validity and efficiency
 Add hints for optimal solution found from above algorithm
 */


public class VirtualWorld extends PApplet{

    private Point curMouse;
    private Point newMouse;
    private Cars curCar;
    private boolean locked;
    public PImage background;

    public String TITLE = "Rush Hour";

    private int xOffset = 0;
    private int yOffset = 0;
    private final int tileWidth = 80;
    private final int tileHeight = 80;
    private final int numRows = 8;
    private final int numCols = 8;

    private static String LOAD_FILE_NAME;
    private final String IMAGE_LIST_FILE_NAME = "imagelist";

    private WorldModel world;
    private Images images;
    private Selection selection;

    public void setup(){
        this.world = new WorldModel(numRows, numCols);
        this.images = new Images(createImageColored(80, 80, 0xC4644F));
        loadImages(IMAGE_LIST_FILE_NAME, images, this);
        loadWorld(world, LOAD_FILE_NAME, images);
        this.background =  loadImage("/Users/notch/Desktop/Nathan Johnson/Projects/Rush Hour/images/Rush_Hour.jpg", "jpg");
        surface.setTitle(TITLE + " " + LOAD_FILE_NAME.substring(LOAD_FILE_NAME.length()-6, LOAD_FILE_NAME.length()-4));
    }

    public void settings(){
        size(640,640);
    }

    public void draw(){
        this.image(background, 0, 0);
        this.world.drawCars(this);
        if (mousePressed){
            newMouse = new Point(mouseX, mouseY);
        }
    }

    public void mousePressed(){
        curMouse = new Point(mouseX/tileWidth, mouseY/tileHeight);
        if (this.world.isOccupied(curMouse)){
            curCar = this.world.getOccupancyCell(curMouse);
            locked = true;
            xOffset = mouseX - curCar.getPosition().x * tileWidth;
            yOffset = mouseY - curCar.getPosition().y * tileHeight;
        } else {locked = false;}
    }

    public void mouseDragged(){
        if (locked){
            this.world.movingCar(curCar, new Point(mouseX, mouseY), new Point(xOffset, yOffset), this);
        }
    }

    public void mouseReleased(){
        locked = false;
    }

    public void loadWorld(WorldModel world, String filename, Images images)
    {
        try {
            Scanner in = new Scanner(new File(filename));
            world.load(in, images);
        } catch (FileNotFoundException e) {
            System.err.println("Invalid Board..." + e.getMessage());
        }
    }

    private static void loadImages(String filename, Images images, PApplet screen)
    {
        try {
            Scanner in = new Scanner(new File(filename));
            images.loadImages(in, screen);
        } catch (FileNotFoundException e) {
            System.err.println(e.getMessage());
        }
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

    public static void chooseBoard(){
        Selection selection = new Selection();
        LOAD_FILE_NAME = selection.selectBoard() ;
    }

    public static void main(String[] args){
        VirtualWorld.chooseBoard();
        PApplet.main(VirtualWorld.class);
    }

    @Override
    public void exitActual() {
    }

}
