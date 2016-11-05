import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

/**
 * Created by jacobs on 05/11/16.
 */
public class Main {
    public static void main(String [] args) throws IOException {
        File file = new File("graphe.txt");
        Graph graph = Graph.creatGraphFromFile(file);
        graph.printGraph();
    }
}
