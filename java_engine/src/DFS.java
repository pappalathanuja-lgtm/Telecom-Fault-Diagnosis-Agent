import java.util.*;
/** Depth-first fault-path exploration. O(V+E) time. */
public final class DFS {
    public List<String> traverse(NetworkGraph g,String start){
        if(g.getNode(start)==null) throw new IllegalArgumentException("Unknown start tower: "+start);
        List<String> order=new ArrayList<>(); Set<String> seen=new LinkedHashSet<>(); visit(g,start,seen,order); return order;
    }
    private void visit(NetworkGraph g,String id,Set<String> seen,List<String> out){seen.add(id);out.add(id);for(Link l:g.getNode(id).getLinks()) if(l.isUp()&&!seen.contains(l.other(id)))visit(g,l.other(id),seen,out);}
}
