import java.io.File;
import java.util.Locale;
import java.util.Scanner;

public class Selection {

    public Selection(){ }

    public String selectBoard(){
        Scanner scanner = new Scanner(System.in);
        System.out.println("Available Boards: ");
        File[] folders = new File("boards").listFiles((dir, name) -> !name.equals(".DS_Store"));
        for (int i = 0; i < folders.length; i++) {
            System.out.println(folders[i].getName().toUpperCase(Locale.ROOT));
            getBoards(folders[i].listFiles());
            System.out.println();
        }
        System.out.println("\nEnter Board: ");
        String input = scanner.nextLine();
        return "boards/" + findBoard(input, folders) + input + ".sav";
    }

    private void getBoards(File[] folder){
        for (int i = 0; i < folder.length; i++) {
            System.out.print(folder[i].getName().substring(0, 2) + ", ");
        }
    }

    private String findBoard(String board, File[] folders){
        board = board + ".sav";
        for (int i = 0; i < folders.length; i++) {
            String level = folders[i].getName();
                    for (int j = 0; j < folders[i].listFiles().length; j++){
                        if (folders[i].listFiles()[j].getName().equals(board)) { return "/" + level + "/";}
            }
        }
        System.out.println("Board Not Found");
        return "";
    }

}
