package newsearch.lucene;

import java.util.ArrayList;
import java.util.Iterator;

import java.util.Collections;

public class NSLucene {
    public static void main (String[] args) {
        ArrayList<DocumentRes> res;
        if (args.length > 0) {
            if (args[0].compareTo ("index") == 0) {
                String[] files = new String [args.length - 1];
                System.arraycopy (args, 1, files, 0, args.length - 1);
                Indexer i = new Indexer ();
                try {
                    i.analyzeFiles (files);
                } catch (Exception e) {
                    System.out.println (e);
                }
            }
            else if (args[0].compareTo ("query") == 0) {
                try {
                    NSSearcher s = new NSSearcher ();
                    res = s.performSearch (args[1]);
                    Collections.sort (res);
                    Iterator<DocumentRes> i = res.iterator ();
                    while (i.hasNext ()) {
                        DocumentRes tmp = (DocumentRes) i.next ();
                        System.out.println (tmp);
                    }

                } catch (Exception e) {
                    e.printStackTrace ();
                }
            }
            else {
                System.out.println ("Unrecognized command");
            }
        }
        else {
            System.out.println ("Type a command");
        }
    }
}