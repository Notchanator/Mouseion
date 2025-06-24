import processing.core.PImage;
import java.util.List;
import java.awt.*;

public class ThreeCar extends Cars{

    public ThreeCar(String newId, Point newPos, List<PImage> newImage, Boolean direction){
        super(newId, newPos, newImage, 3, direction);
    }
}
