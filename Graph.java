import java.io.*;
import java.util.HashMap;

/**
 * Created on 04/11/16.
 */


public class Graph {
    private HashMap<String,Node> graphMap;
    private final int graphOrder;

    public Graph(int graphOrder){
        this.graphMap = new HashMap<String, Node>();
        this.graphOrder = graphOrder;
    }

    public static Graph creatGraphFromFile(File file) throws IOException {
        Graph graph;
        FileReader readFile = new FileReader(file);
        BufferedReader br = new BufferedReader(readFile);
        graph = new Graph(Integer.parseInt(br.readLine()));
        graph.addEachNodesDebtsFromFile(br, readFile, file);
        return graph;
    }

    private void addEachNodesDebtsFromFile(BufferedReader br,FileReader readFile, File file) throws IOException {
        int i = 0;
        String line;
        while ((i < graphOrder) && ((line = br.readLine()) != null)) {
            String output[];
            output = line.split(" ");
            if(graphMap.containsKey(output[0])) {
                continue;
            }
            Node node = new Node(output[0]);
            graphMap.put(node.getName(), node);
            i++;
        }

        readFile.close();
        readFile = new FileReader(file);
        br = new BufferedReader(readFile);
        br.readLine();

        while ((line = br.readLine()) != null) {
            String output[];
            output = line.split(" ");
            Node node_from = graphMap.get(output[0]);
            if(!graphMap.containsKey(output[1])){
                Node node = new Node(output[1]);
                graphMap.put(node.getName(), node);
            }
            Node node_to = graphMap.get(output[1]);
            int amount = Integer.parseInt(output[2]);
            node_from.addDebt(node_to, amount);
        }
    }

    
    public void printGraph(){
        for (String name: graphMap.keySet()){
            Node node = graphMap.get(name);
            System.out.format("Node %s has %s connexions %n Debts: %n", name, node.getNumberOfConnexions());
            for(Node node_to : node.getDebts().keySet()){
                System.out.format("Node %s amount %s, ",node_to.getName(), node.getDebts().get(node_to));
            }
            System.out.println();
        }
    }
}
