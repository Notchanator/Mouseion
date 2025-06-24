import processing.core.PImage;
import java.util.List;
import java.awt.*;

public abstract class Cars {

    protected String id;
    protected Point position;
    protected List<PImage> image;
    protected boolean horizontal;
    protected int size;

    public Cars(String newId, Point newPos, List<PImage> newImage, int newSize, boolean direction){
        this.id = newId;
        this.position = newPos;
        this.image = newImage;
        this.horizontal = direction;
        this.size = newSize;
    }

    public Point getPosition() {return this.position;}

    public List<PImage> getImage() {return this.image;}

    public boolean getDirection() {return this.horizontal;}

    public int getSize() {return this.size;}

    public void setPosition(Point pos) {this.position = pos;}

}
