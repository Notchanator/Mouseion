import processing.core.PImage;
import java.util.List;
import java.awt.*;

public class TwoCar extends Cars{

    public TwoCar(String newId, Point newPos, List<PImage> newImage, Boolean direction){
        super(newId, newPos, newImage, 2, direction);
    }
}
