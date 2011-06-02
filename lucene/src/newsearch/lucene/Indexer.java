package newsearch.lucene;

import java.util.Scanner;

import java.lang.StringBuilder;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.File;

import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.util.Version;
import org.apache.lucene.store.SimpleFSDirectory;



public class Indexer {
    private IndexWriter ind = null;
    private SimpleFSDirectory dir = null;

    public Indexer () {
        try {
            dir = new SimpleFSDirectory (new File ("index.ind"));
        }
        catch (Exception e) {
            System.out.println (e);
        }
    }

    private IndexWriter getIndexWriter () throws Exception {
        if (ind == null) {
            ind = new IndexWriter (dir, new IndexWriterConfig (Version.LUCENE_31, new StandardAnalyzer (Version.LUCENE_31)));
        }
        return ind;
    }

    private void closeIndexWriter () throws Exception {
        if (ind != null) {
            ind.close ();
        }
    }

    private Document getDoc (String cont, String f) {
        Document res = new Document ();
        String id = getId (f);
        System.out.println ("Indexing file: " + id);
        res.add (new Field ("id", id, Field.Store.YES, Field.Index.NO));
        res.add (new Field ("content", cont, Field.Store.YES, Field.Index.ANALYZED));
        return res;
    }


    private String getId (String path) {
        String id = "";
        String PS = File.separator;
        try {
                id = path.substring (path.lastIndexOf(PS) + 1, path.lastIndexOf("."));
        } catch (Exception e) {
                id = path.substring (0, path.lastIndexOf("."));
        }
        return id;
    }

    private String readContent (String file) throws Exception {
        StringBuilder cont = new StringBuilder ();
        String NL = System.getProperty ("line.separator");
        Scanner scn = new Scanner (new FileInputStream (file));
        try {
            while (scn.hasNextLine ()){
                cont.append (scn.nextLine () + NL);
            }
        }
        finally{
            scn.close ();
        }
        return cont.toString ();
    }

    public void analyzeFiles (String[] files) throws Exception {
        IndexWriter iw = getIndexWriter ();
        for (String f : files) {
            String cont = readContent (f);
            Document d = getDoc (cont, f);
            iw.addDocument (d);
        }
        closeIndexWriter ();
    }
}