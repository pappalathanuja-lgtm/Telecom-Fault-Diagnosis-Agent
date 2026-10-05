import java.util.*;
public final class FaultPath {
    private final List<String> nodes; private final List<String> links;
    public FaultPath(List<String> nodes,List<String> links){this.nodes=List.copyOf(nodes);this.links=List.copyOf(links);}
    public List<String> getNodes(){return nodes;} public List<String> getLinks(){return links;}
}
