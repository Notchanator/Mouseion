Better way of defining difference between colors for my BFS search threshold
    The sRGB color space isn't perceptually uniformly accurate. 
        Meaning that a fixed distance can have perceptual differences from different starting colors
    CIELAB seems to be a better perceptually uniform color space, with its own metric DeltaE
        DeltaE has a threshold of 1.0 indicating different colors 

Convert RGB colors to CIELAB
    Calculate DeltaE(2000)


Things to Do
    - If CIELAB works out convert all colors before instead during each calculation


While it is nice to keep old methodology and colorSimplifiers it is overkill.
In almost all cases the K-means outpreforms the other methods, and I think when it doens't
outpreform it is ok to consider that good enough.

Use Streamlit since to build the app that houses the ColorSimplifier application. 