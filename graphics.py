import pickle

def load_pickles():
    cl = pickle.load(open( "pk/cl.p", "rb" ) )
    clusters = pickle.load( open( "pk/clusters.p", "rb" ) )
    categs = pickle.load( open( "pk/categs.p", "rb" ) )
    colors = pickle.load(open( "pk/colors.p", "rb" ) )
    df = pickle.load(open( "pk/df.p", "rb" ) )
    dflabel = pickle.load(open( "pk/dflabel.p", "rb" ) )
    return None