import java.util.*;

/** Encapsulated tower vertex in the telecom topology. */
public final class Node {
    private final String id;
    private final List<Link> links = new ArrayList<>();
    public Node(String id) { this.id = Objects.requireNonNull(id); }
    public String getId() { return id; }
    public List<Link> getLinks() { return Collections.unmodifiableList(links); }
    public void addLink(Link link) { links.add(Objects.requireNonNull(link)); }
}
