package newsearch.lucene;

import java.lang.Comparable;


public class DocumentRes implements Comparable {
    public String id;
    public float score;

    public DocumentRes (String id, float score) {
        this.id = id;
        this.score = score;
    }

    public int compareTo (Object dr) {
        DocumentRes other = (DocumentRes) dr;
        if (this.score == other.score) return 0;
        else if (this.score > other.score) return 1;
        else return -1;
    }

    public String toString () {
        return "(" + this.score + ", " + this.id + ")";
    }
}