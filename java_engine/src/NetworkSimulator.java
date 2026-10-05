public final class NetworkSimulator {
    public NetworkGraph build(String json){
        NetworkGraph g=new NetworkGraph();
        java.util.regex.Matcher nodes=java.util.regex.Pattern.compile("\\\"tower_id\\\"\\s*:\\s*\\\"([^\\\"]+)\\\"").matcher(json);
        while(nodes.find())g.addNode(nodes.group(1));
        java.util.regex.Matcher links=java.util.regex.Pattern.compile("\\{[^{}]*\\\"link_id\\\"[^{}]*\\}").matcher(json);
        while(links.find()){
            String obj=links.group();String id=get(obj,"link_id"),a=get(obj,"source"),b=get(obj,"destination"),status=get(obj,"status");
            if(id!=null&&a!=null&&b!=null)g.addLink(new Link(id,a,b,!"DOWN".equalsIgnoreCase(status)));
        }
        if(g.getNodes().isEmpty())throw new IllegalArgumentException("JSON request contains no tower nodes");return g;
    }
    private String get(String s,String k){java.util.regex.Matcher m=java.util.regex.Pattern.compile("\\\""+k+"\\\"\\s*:\\s*\\\"([^\\\"]*)\\\"").matcher(s);return m.find()?m.group(1):null;}
}
