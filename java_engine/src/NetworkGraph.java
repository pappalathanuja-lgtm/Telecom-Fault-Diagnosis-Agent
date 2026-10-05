import java.util.*;
public final class NetworkGraph {
    private final Map<String,Node> nodes=new LinkedHashMap<>(); private final Map<String,Link> links=new LinkedHashMap<>();
    public Node addNode(String id){return nodes.computeIfAbsent(id,Node::new);}
    public void addLink(Link link){ if(links.containsKey(link.getId())) throw new IllegalArgumentException("Duplicate link: "+link.getId()); Node a=nodes.get(link.getSource()), b=nodes.get(link.getDestination()); if(a==null||b==null) throw new IllegalArgumentException("Link references an unknown tower"); links.put(link.getId(),link); a.addLink(link); b.addLink(link); }
    public Collection<Node> getNodes(){return Collections.unmodifiableCollection(nodes.values());}
    public Node getNode(String id){return nodes.get(id);}
    public Collection<Link> getLinks(){return Collections.unmodifiableCollection(links.values());}
}
