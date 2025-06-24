import processing.core.PApplet;
import java.awt.*;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

public class WorldModel {

    public int numRows;
    public int numCols;
    private Cars occupancy[][];
    public Set<Cars> cars;

    private final int PROPERTY_KEY = 0;
    private final String RED_KEY = "RedCar";
    private final String TWO_HOR_KEY = "TwoCarHor";
    private final String THREE_HOR_KEY = "ThreeCarHor";
    private final String TWO_VERT_KEY = "TwoCarVert";
    private final String THREE_VERT_KEY = "ThreeCarVert";

    private final int TILE_WIDTH = 80;
    private final int TILE_HEIGHT = 80;

    private final int VERTICAL = 1;
    private final int HORIZONTAL = 0;

    public WorldModel(int numRows, int numCols){
        this.numCols =  numCols;
        this.numRows = numRows;
        this.occupancy = new Cars[numRows][numCols];
        this.cars = new HashSet<>();
    }

    public boolean carWithinBounds(Cars car){
        int size = car.getSize() - 1;
        if (car.getDirection()) {
            Point pos = car.getPosition();
            return pos.y > 0 && pos.y < this.numRows - 1 &&
                    pos.x > 0 && pos.x < this.numCols - 1 &&
                    pos.x + size < this.numCols - 1;
        }
            Point pos = car.getPosition();
            return pos.y > 0 && pos.y < this.numRows - 1 &&
                    pos.x > 0 && pos.x < this.numCols - 1 &&
                    pos.y + size < this.numRows - 1;
    }

    public boolean pointWithinBounds(Point pos){
        return pos.y > 0 && pos.y < this.numRows - 1 &&
                pos.x > 0 && pos.x < this.numCols - 1;
    }

    protected Cars getOccupancyCell(Point pos) {return this.occupancy[pos.y][pos.x];}

    protected void setOccupancyCell(Point pos, Cars car) {
        for (int i = 0; i < car.getSize(); i++)
            if (car.getDirection()){
                setOccupancyCellAt(new Point(pos.x + 1*i, pos.y), car);
            } else {
                setOccupancyCellAt(new Point(pos.x, pos.y + 1*i), car);
            }
    }

    protected void setOccupancyCellAt(Point pos, Cars car){
        this.occupancy[pos.y][pos.x] = car;
    }

    public boolean isOccupied(Point pos)
    {
        return this.pointWithinBounds(pos) &&
                this.getOccupancyCell(pos) != null;
    }

    public void tryAddCar(Cars car)
    {
        if (this.isOccupied(car.getPosition()))
        {
            throw new IllegalArgumentException("position occupied");
        }

        this.addCar(car);
    }

    public void addCar(Cars car)
    {
        if (this.carWithinBounds(car))
        {
            this.setOccupancyCell(car.getPosition(), car);
            this.cars.add(car);
        }
    }

    public void movingCar(Cars car, Point mouse, Point offset, PApplet screen){
        if (car.getDirection()){
            for (int i = 0; i < car.getSize(); i++)
                this.setOccupancyCellAt(new Point(car.getPosition().x + 1*i, car.getPosition().y), null);
            Point newPos = new Point((mouse.x - offset.x)/TILE_WIDTH , car.getPosition().y);
            for (int i = 0; i < car.getSize(); i++){
                Point carPart = new Point(newPos.x + 1*i, newPos.y);
                if ((!this.pointWithinBounds(carPart) || this.getOccupancyCell(carPart) != null
                || newPos.distance(car.getPosition()) > 1) && !this.isVictory(car, screen)) {
                    this.setOccupancyCell(car.getPosition(), car);
                    return;} }
            car.setPosition(newPos);
            this.setOccupancyCell(car.getPosition(), car);
        } else {
            for (int i = 0; i < car.getSize(); i++)
                this.setOccupancyCellAt(new Point(car.getPosition().x, car.getPosition().y + 1*i), null);
            Point newPos = new Point(car.getPosition().x, (mouse.y - offset.y)/TILE_WIDTH);
            for (int i = 0; i < car.getSize(); i++){
                Point carPart = new Point(newPos.x, newPos.y + 1*i);
                if (!this.pointWithinBounds(carPart) || this.getOccupancyCell(carPart) != null || newPos.distance(car.getPosition()) > 1) {
                    this.setOccupancyCell(car.getPosition(), car);
                    return;} }
            car.setPosition(newPos);
            this.setOccupancyCell(car.getPosition(), car);
        }
    }

    public void load(Scanner in, Images images)
    {
        int lineNumber = 0;
        while (in.hasNextLine())
        {
            try
            {
                if (!processLine(in.nextLine(), images))
                {
                    System.err.println(String.format("invalid entry on line %d",
                            lineNumber));
                }
            }
            catch (NumberFormatException e)
            {
                System.err.println(String.format("invalid entry on line %d",
                        lineNumber));
            }
            catch (IllegalArgumentException e)
            {
                System.err.println(String.format("issue on line %d: %s",
                        lineNumber, e.getMessage()));
            }
            lineNumber++;
        }
    }

    private boolean processLine(String line, Images images)
    {
        String[] properties = line.split("\\s");
        Parse parse = new Parse(properties, images, this);
        if (properties.length > 0)
        {
            switch (properties[PROPERTY_KEY])
            {
                case RED_KEY:
                    return parse.redCar();
                case TWO_HOR_KEY:
                    return parse.twoCar(HORIZONTAL);
                case TWO_VERT_KEY:
                    return parse.twoCar(VERTICAL);
                case THREE_HOR_KEY:
                    return parse.threeCar(HORIZONTAL);
                case THREE_VERT_KEY:
                    return parse.threeCar(VERTICAL);
            }
        }
        return false;
    }

    public void drawCars(PApplet screen){
        for (Cars car: this.cars){
            screen.image(car.getImage().get(0), car.getPosition().x * TILE_WIDTH, car.getPosition().y * TILE_HEIGHT);
        }
    }

    private boolean isVictory(Cars car, PApplet screen){
        if (car.id == "RedCar" && car.getPosition().x == 5 && car.getPosition().y == 3){
            // Closes the current board
            VirtualWorld.chooseBoard();
            screen.setup();
            return true;
        }
        return false;
    }

}
