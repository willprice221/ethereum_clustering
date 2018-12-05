<br>

### Unmasking Ethereum Users

#### Categorizing addresses using patterns in transaction activity

![](https://cdn-images-1.medium.com/max/1000/1*BxydgpDx7w2ZLFB-Ewc6ng.jpeg)
<span class="figcaption_hack">Image credit: Reddit user [IanJMeikle](https://www.reddit.com/user/ianjmeikle) </span>

#### Introduction

Ethereum users may be anonymous, but their addresses are unique identifiers that
leave a trail publicly visible on the blockchain.

Based on address transaction activity, I used Python to build a clustering
algorithm to divide Ethereum users into distinct behavioral subgroups.

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

Ether is stored in cryptographically secured accounts called **addresses. **

#### Motivation

Many people believe that cryptocurrencies offer digital anonymity, and there is
some truth to that belief. In fact, anonymity is the core mission of
[Monero](https://www.getmonero.org/) and [ZCash](https://z.cash/).

Ethereum, however, is more widely used, and its broad flexibility results in a
rich, public dataset of transactional behavior. Because Ethereum addresses are
unique identifiers whose ownership does not change, their activity can be
tracked, aggregated, and analyzed.

Here, I attempt to create **user archetypes** by effectively clustering the
Ethereum address space. This opens up a wide array of potential applications,
including trading and
[AML](https://en.wikipedia.org/wiki/Money_laundering#Combating) activities.

#### Results

Participants in the Ethereum ecosystem are can be separated by patterns in their
transaction activity. Addresses known to belong to exchanges, miners, and
[ICOs](https://www.investopedia.com/terms/i/initial-coin-offering-ico.asp)
qualitatively show that the results of clustering are accurate.

![](https://cdn-images-1.medium.com/max/800/1*Vn4bKT8Ajvnqr5KkPyxpeA.gif)

### Technical Details

Feel free to skip to **Interpreting the Results** below.

#### Feature Engineering

The Ethereum transaction dataset is hosted  on [Google
BigQuery](https://cloud.google.com/blog/products/data-analytics/ethereum-bigquery-public-dataset-smart-contract-analytics).
Using the 40,000 addresses with the highest ether balances, I created 25
features to characterize differences in user behavior.

![](https://cdn-images-1.medium.com/max/800/1*Dkza60Nx4wJFG1EqcleEvQ.jpeg)
<span class="figcaption_hack">Features derived for each address</span>

#### Choosing  the Appropriate Number of Clusters

Using [silhouette
analysis](https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html),
I determined the optimal number of clusters to be around 8.

This choice minimizes the number of samples with negative silhouette scores,
which indicate that a sample may be assigned to the wrong cluster.

![](https://cdn-images-1.medium.com/max/800/1*J_EePhAcrfdwEhS0cAF7oA.png)

#### But how do we know if it’s working?

By scraping data from the[ Etherscan.io](https://etherscan.io/) block explorer,
I gathered  crowdsourced labels for 125 addresses in my dataset.

The majority of labels fell into three categories:

*exchanges, miners, and ICO wallets.*

Clustering is an unsupervised machine learning technique, so I could not use
labels to  train my model. Instead, I used them to assign **user archetypes **to
clusters, based on the highest label density for each cluster. [Results can be
found
here](https://gist.github.com/willprice221/ef10c1622a5e6daeccf59c4251b54682#file-clusterlabels-txt).

![](https://cdn-images-1.medium.com/max/800/1*e7f60yRsOdj1SE2dyYBTzQ.png)
<span class="figcaption_hack">2D visualization of initial clustering. Known addresses on the left.</span>

#### Re-clustering

After the initial clustering was performed, I could not distinguish between
*exchanges* and *miners*. Since the majority of both types of addresses resided
in cluster #2, I attempted to tease out more signal by re-clustering, using
only the addresses in that cluster. Here, the optimal number of sub-clusters was
3.

![](https://cdn-images-1.medium.com/max/800/1*oFqDdga_jzmgcBapZVPBdQ.png)

![](https://cdn-images-1.medium.com/max/800/1*Zfu_4pykQJ4UbYs3rUgiBA.png)
<span class="figcaption_hack">Improved separation of exchanges and miners. Known addresses on the left.</span>

By substituting results from re-clustering into the original analysis, we end up
with 10 clusters in total.

![](https://cdn-images-1.medium.com/max/800/1*wf36RPOxvKzEL1gMvm4ktw.png)
<span class="figcaption_hack">2D visualization of final clustering results. Known addresses on the left.</span>

### Interpreting the Results

We can draw conclusions about user behavior based on the corresponding cluster
centroids.

![](https://cdn-images-1.medium.com/max/800/1*MRKCJCziAzog7Gr0aTjUig.png)
<span class="figcaption_hack">Radar plot — cluster centroid address features</span>

#### Exchanges

* High ether balance
* High incoming and outgoing transaction volume
* Highly irregular  time between transactions

Exchanges are the banks of the crypto space. These results are intuitive.

#### Miners

* Low ether balance
* Small average transaction size
* More  regular time between transactions

Miners secure the blockchain by expending computational power, and are rewarded
with ether. Groups of miners often “pool” their resources to reduce variance in
payouts, splitting the proceeds based on resources contributed.

#### ICO Wallets

* High ether balance
* Small number of large transactions
* Most regular time between transactions

ICOs (Initial Coin Offerings) are a common fundraising method for crypto
startups. It makes sense that these startups would have large war chests, and
periodically sell  large amounts to cover regular business expenses.

#### Other categories

The remaining clusters did not contain enough labeled addresses for me to make
any predictions with confidence.

Take a look at the labeled addresses in each cluster
[here.](https://gist.github.com/willprice221/ef10c1622a5e6daeccf59c4251b54682#file-clusterlabels-txt)

The heat map below shows how similar the clusters are to each other.

![](https://cdn-images-1.medium.com/max/800/1*YKPKzdI_pYG1eA72r6xDeQ.png)
<span class="figcaption_hack">ICO Wallets: 3, Exchange: 100, Mining:101, Exchange#2: 102</span>

* The *Exchange (100) *and *Mining (101) *clusters are highly similar. This is
because they are a result of the second round of clustering.
* Addresses in cluster 7 have a large amount of smart contract activity.
* Clusters 0 and 5 are highly distinct.

#### **Can you identify any of these user groups?**

![](https://cdn-images-1.medium.com/max/1000/1*HpQ2W-nnhD2-nu5lscVN_w.png)
<span class="figcaption_hack">Radar plots for each cluster. Cluster numbers in the 100s are a result of
re-clustering.</span>

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
