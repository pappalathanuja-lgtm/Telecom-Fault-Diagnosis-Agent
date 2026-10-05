import java.util.*;
/** Breadth-first traversal returns levels; O(V+E) time. */
public final class BFS {
    public List<List<String>> levels(NetworkGraph g,String start){
        if(g.getNode(start)==null) throw new IllegalArgumentException("Unknown start tower: "+start);
        List<List<String>> levels=new ArrayList<>(); Set<String> seen=new HashSet<>(); Queue<String> q=new ArrayDeque<>();q.add(start);seen.add(start);
        while(!q.isEmpty()){int n=q.size();List<String> level=new ArrayList<>();for(int i=0;i<n;i++){String id=q.remove();level.add(id);for(Link l:g.getNode(id).getLinks()){String next=l.other(id);if(l.isUp()&&seen.add(next))q.add(next);}}levels.add(level);}return levels;
    }
}
