import processing.core.PApplet;
import processing.core.PImage;
import java.util.*;

public class Images {

    private Map<String, List<PImage>> images;
    private List<PImage> defaultImages;

    public Images(PImage defaultImage) {
        this.images = new HashMap<>();
        defaultImages = new LinkedList<>();
        defaultImages.add(defaultImage);
    }

    public List<PImage> getImageList(String key) {
        return this.images.getOrDefault(key, this.defaultImages);
    }

    public void loadImages(Scanner in, PApplet screen) {
        int lineNumber = 0;
        while (in.hasNextLine()) {
            try {
                processImageLine(in.nextLine(), screen);
            } catch (NumberFormatException e) {
                System.out.println(String.format("Image format error on line %d",
                        lineNumber));
            }
            lineNumber++;
        }
    }

    private void processImageLine(String line, PApplet screen) {
        String[] attrs = line.split("\\s");
        if (attrs.length >= 2) {
            String key = attrs[0];
            PImage img = screen.loadImage(attrs[1]);
            if (img != null && img.width != -1) {
                List<PImage> imgs = this.getImages(key);
                imgs.add(img);

            }
        }
    }

    private List<PImage> getImages(String key) {
        List<PImage> imgs = this.images.get(key);
        if (imgs == null) {
            imgs = new LinkedList<>();
            this.images.put(key, imgs);
        }
        return imgs;
    }
}
