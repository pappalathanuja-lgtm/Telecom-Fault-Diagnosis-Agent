import java.util.Objects;

/** Undirected communication link represented as a graph edge. */
public final class Link {
    private final String id, source, destination;
    private final boolean up;
    public Link(String id, String source, String destination, boolean up) {
        this.id=Objects.requireNonNull(id); this.source=Objects.requireNonNull(source); this.destination=Objects.requireNonNull(destination); this.up=up;
    }
    public String getId(){return id;} public String getSource(){return source;} public String getDestination(){return destination;} public boolean isUp(){return up;}
    public String other(String node){ if(source.equals(node)) return destination; if(destination.equals(node)) return source; throw new IllegalArgumentException("Node is not incident to link " + id); }
}
