/** A graph fault marker, such as a failed fiber link. */
public final class Fault {
    private final String type, linkId;
    public Fault(String type, String linkId){this.type=type;this.linkId=linkId;}
    public String getType(){return type;} public String getLinkId(){return linkId;}
}
