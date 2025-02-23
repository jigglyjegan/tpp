import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

### NOTE: Important, need to convert the processed docs to array before
# inputting into NMF

# docs_arr = np.asarray(docs)


def plot_top_words(model, feature_names, n_top_words, title):
    '''
    Parameters
    ----------
    model : sklearn.estimator
        The fitted nmf estimator.

    feature_names : np.array
        The feature names used for training (Selected by TF-IDF Vectorizer).
    
    n_top_words : int
        The number of top words to show for each topic in plot.
    
    title : str
        The main title of the plot.
    '''
    fig, axes = plt.subplots(1, 5, figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[: -n_top_words - 1 : -1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]

        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f"Topic {topic_idx +1}", fontdict={"fontsize": 30})
        ax.invert_yaxis()
        ax.tick_params(axis="both", which="major", labelsize=20)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)

    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    plt.show()

def run_nmf(docs, num_topics):
    '''
    Parameters
    ----------
    docs : np.array
        An array of documents. Note that each document is a string of the processed text.

    num_topics : int
        Number of topics to learn.
    
    Returns
    ----------
    nmf : sklearn.estimator
        The fitted nmf sklearn estimator instance.
    '''
    tfidf_params = {'min_df': 0.0008, 
                    'max_df': 0.90, 
                    'max_features': 500, 
                    'norm': 'l1'}
    nmf_params = {'n_components': num_topics, 
                'alpha_W': 3.108851387228361e-05, 
                'alpha_H': 8.312434671077156e-05, 
                'l1_ratio': 0.3883534426209613, 
                'beta_loss': 'kullback-leibler', 
                'init': 'nndsvda', 
                'solver': 'mu', 
                'max_iter': 1000, 
                'random_state': 4013, 
                'tol': 0.0001}
    
    tfidf_vectorizer = TfidfVectorizer(**tfidf_params)
    tfidf = tfidf_vectorizer.fit_transform(docs)

    tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()

    nmf = NMF(**nmf_params)
    nmf.fit(tfidf)

    '''
    W is the Document-Topic matrix. 
    Each row in W represents the Document and the entries represents the Document's rank in a Topic.
    H is the Topic-Word matrix (weighting). 
    Each column in H represents a Word and the entries represents the Word's rank in a Topic.
    Matrix multiplication of the factored components, W x H results in the input Document-Word matrix.
    '''

    W = nmf.fit_transform(tfidf)
    H = nmf.components_

    ### Plot top words for each topic
    plot_top_words(nmf, tfidf_feature_names, 10, "Topics in NMF model (KL Divergence Loss)")

    return nmf
