import java.util.HashMap;
import java.util.Set;

/**
 * Created by jacobs on 05/11/16.
 */

public class Node {
    private String name;
    private HashMap<Node, Integer> debts;
    private int numberOfConnexions;

    public Node(String name) {
        this.name = name;
        this.debts = new HashMap<>();
        this.numberOfConnexions = 0;
    }

    public String getName() {
        return name;
    }

    public int getNumberOfConnexions() {
        return numberOfConnexions;
    }

    public void addDebt(Node node_to, int amount) {
        debts.put(node_to, amount);
        numberOfConnexions++;
    }

    public HashMap<Node, Integer> getDebts() {
        return debts;
    }
}
