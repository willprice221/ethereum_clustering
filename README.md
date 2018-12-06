# Clustering Ethereum Addresses

## Categorizing addresses using patterns in transaction activity

![](https://cdn-images-1.medium.com/max/1000/1*BxydgpDx7w2ZLFB-Ewc6ng.jpeg)
<span class="figcaption_hack">Image credit: Reddit user I[anJMeikle](https://www.reddit.com/user/ianjmeikle)</span>

#### Introduction

Ethereum users may be anonymous, but their addresses are unique identifiers that
leave a trail publicly visible on the blockchain.

I built a clustering algorithm based on transaction activity that divides
Ethereum users into distinct behavioral subgroups. It can predict whether an
address belongs to an exchange, miner, or ICO wallet.

The database was constructed using SQL, and the model was coded in Python.
Source code is available on
[GitHub](https://github.com/willprice221/ethereum_clustering).

![](https://cdn-images-1.medium.com/max/800/1*S7Z4GMFkSuezVdtjO6htyw.gif)
<span class="figcaption_hack">3D representation of Ethereum address feature space using
[T-SNE](https://lvdmaaten.github.io/tsne/)</span>

#### Background

The Ethereum blockchain is a platform for decentralized applications called
**smart contracts. **These contracts are often used to represent other assets.
These assets can represent physical objects in the real world (like real estate
titles) or be purely digital objects (such as [utility
tokens](https://medium.com/coinmonks/utility-tokens-a-general-understanding-f6a5f9699cc0)).

The computations required to execute smart contracts are paid for in **ether**,
the native currency of the ecosystem.

Ether is stored in cryptographically secured accounts called **addresses.**

#### Motivation

Many people believe that cryptocurrencies offer digital anonymity, and there is
some truth to that belief. In fact, anonymity is the core mission of
[Monero](https://www.getmonero.org/) and [ZCash](https://z.cash/).

Ethereum, however, is more widely used, and its broad flexibility results in a
rich, public dataset of transactional behavior. Because Ethereum addresses are
unique identifiers whose ownership does not change, their activity can be
tracked, aggregated, and analyzed.

Here, I attempt to create **user archetypes** by effectively clustering the
Ethereum address space. These archetypes could be used to predict the owner of
an unknown address.

This opens up a wide array of applications:

* understanding network activity
* enhancing trading strategies
* improving [AML](https://en.wikipedia.org/wiki/Money_laundering#Combating)
activities

#### Results

Participants in the Ethereum ecosystem can be separated by patterns in their
transaction activity. Addresses known to belong to exchanges, miners, and
[ICOs](https://www.investopedia.com/terms/i/initial-coin-offering-ico.asp)
qualitatively show that the results of clustering are accurate.

![](https://cdn-images-1.medium.com/max/800/1*_Ar6rUk6jC9vtDFgq0KdNw.gif)

### Technical Details

Feel free to skip to **Interpreting the Results** below.

#### Feature Engineering

The Ethereum transaction dataset is hosted on [Google
BigQuery](https://cloud.google.com/blog/products/data-analytics/ethereum-bigquery-public-dataset-smart-contract-analytics).
Using the 40,000 addresses with the highest ether balances, I created 25
features to characterize differences in user behavior.

![](https://cdn-images-1.medium.com/max/800/1*Dkza60Nx4wJFG1EqcleEvQ.jpeg)
<span class="figcaption_hack">Features derived for each address</span>

#### Choosing the Appropriate Number of Clusters

Using [silhouette
analysis](https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html),
I determined the optimal number of clusters to be roughly 8.

This choice minimizes the number of samples with negative silhouette scores,
which indicate that a sample may be assigned to the wrong cluster.

#### But how do we know if it’s working?

By scraping data from the[ Etherscan.io](https://etherscan.io/) block explorer,
I gathered crowdsourced labels for 125 addresses in my dataset.

The majority of labels fell into three categories:

*exchanges, miners, and ICO wallets.*

Clustering is an unsupervised machine learning technique, so I could not use
labels to train my model. Instead, I used them to assign **user archetypes **to
clusters, based on the highest label density for each cluster. [Results can be
found
here](https://gist.github.com/willprice221/ef10c1622a5e6daeccf59c4251b54682#file-clusterlabels-txt).

<span class="figcaption_hack">2D visualization of initial clustering. Known addresses on the left.</span>

#### Re-clustering

*Exchange* and *miner *addresses were mixed together in the same cluster at
first. To separate them, I performed a second round of clustering, using only
the addresses in that cluster.

By changing the dissimilarity measure from *euclidean distance *to* cosine
distance, *I dramatically improved separation between exchanges and miners.

<span class="figcaption_hack">Improved separation of exchanges and miners. Known addresses on the left.</span>

By substituting results from re-clustering into the original analysis, we end up
with 9 clusters.

<span class="figcaption_hack">2D visualization of final clustering results. Known addresses on the left.</span>

### Interpreting the Results

We can draw conclusions about user behavior based on the corresponding cluster
centroids.

<span class="figcaption_hack">Radar plot — cluster centroid address features</span>

#### Exchanges

* High ether balance
* High incoming and outgoing transaction volume
* Highly irregular time between transactions

Exchanges are the banks of the crypto space. These results are intuitive.

#### Miners

* Low ether balance
* Small average transaction size
* More regular time between transactions

Miners secure the blockchain by expending computational power, and are rewarded
with ether. Groups of miners often “pool” their resources to reduce variance in
payouts, splitting the proceeds based on resources contributed.

#### ICO Wallets

* High ether balance
* Small number of large transactions
* Most regular time between transactions

ICOs (Initial Coin Offerings) are a common fundraising method for crypto
startups. It makes sense that these startups would have large war chests, and
periodically sell large amounts to cover regular business expenses.

#### Other categories

* The *Exchange *and *Mining *clusters are highly similar, as they were created in
the second round of clustering.
* Addresses in cluster 7 have a large amount of smart contract activity.
* Clusters 2 and 5 are highly distinct.

#### **Can you identify any of these user groups?**

### Next Steps

Expanding on this work would allow a more nuanced view of Ethereum blockchain
data. Here are some particularly interesting areas:

* Adding features based on graph theory & network analysis
* Distinguishing bots from humans
* Expanding smart contract analysis
* Repeating analysis for [ERC-20
token](https://cointelegraph.com/explained/erc-20-tokens-explained) transaction
activity

### Questions? Suggestions?

You can find me on [Twitter](https://twitter.com/willprice221) or
[LinkedIn](https://www.linkedin.com/in/willprice221/).

### References

[Etherscan.io Label Word Cloud](https://etherscan.io/labelcloud)

[Mastering Ethereum](https://github.com/ethereumbook/ethereumbook)

[Characterizing the Ethereum Address
Space](http://cs229.stanford.edu/proj2017/final-reports/5244232.pdf)

[A Fistful of Bitcoins: Characterizing Payments Among Men with No
Names](https://cseweb.ucsd.edu/~smeiklejohn/files/imc13.pdf)

*Thanks to Brandon Martin-Anderson, Alex Cuevas, John Braunlin, and Eric Bragas
for reviewing drafts of this article.*

* [Blockchain](https://towardsdatascience.com/tagged/blockchain?source=post)
* [Data Science](https://towardsdatascience.com/tagged/data-science?source=post)
* [Machine
Learning](https://towardsdatascience.com/tagged/machine-learning?source=post)
* [Ethereum](https://towardsdatascience.com/tagged/ethereum?source=post)
* [Cryptocurrency](https://towardsdatascience.com/tagged/cryptocurrency?source=post)

### [Will Price](https://towardsdatascience.com/@will_price)

Data scientist and systems thinker. Interested in cryptocurrency and behavioral
economics.

### [Towards Data Science](https://towardsdatascience.com/?source=footer_card)

Sharing concepts, ideas, and codes.
