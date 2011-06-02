package newsearch.lucene;

import org.apache.lucene.document.Document;
import org.apache.lucene.queryParser.ParseException;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.util.Version;
import org.apache.lucene.store.SimpleFSDirectory;
import org.apache.lucene.search.Collector;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.Scorer;
import org.apache.lucene.search.Searcher;
import org.apache.lucene.document.Document;

import java.io.IOException;
import java.io.File;

public class NSSearcher {
    private StandardAnalyzer sa = null;
    private SimpleFSDirectory dir = null;
    private IndexSearcher searcher = null;
    private QueryParser parser = null;
    private int MAX_RES = 100;

    /** Creates a new instance of SearchEngine */
    public NSSearcher () throws IOException {
        sa = new StandardAnalyzer (Version.LUCENE_31);
        dir = new SimpleFSDirectory (new File ("index.ind"));
        searcher = new IndexSearcher (dir);
        parser = new QueryParser(Version.LUCENE_31, "content", sa);
    }

    public void performSearch (String queryString) throws IOException, ParseException {
        Query query = parser.parse (queryString);
        doStreamingSearch (searcher, query);

    }

    private void doStreamingSearch (final Searcher searcher, Query query) throws IOException {
        Collector streamingHitCollector = new Collector() {
                private Scorer scorer;
                private int docBase;

                // simply print docId and score of every matching document
                @Override
                    public void collect(int doc) throws IOException {
                    Document d = searcher.doc (doc);
                    System.out.println("doc=" + d.get("id") + " score=" + scorer.score());
                }

                @Override
                    public boolean acceptsDocsOutOfOrder() {
                    return true;
                }

                @Override
                    public void setNextReader(IndexReader reader, int docBase)
                    throws IOException {
                    this.docBase = docBase;
                }

                @Override
                    public void setScorer(Scorer scorer) throws IOException {
                    this.scorer = scorer;
                }

            };

        searcher.search(query, streamingHitCollector);
    }
}