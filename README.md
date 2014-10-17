Fair Shuffle
============

Fairly shuffle list, using unpredictable but fair and verifiable values from the Bitcoin blockchain.

This is nothing complicated, but I think this is a new algorithm/method I have invented, and once again demonstrates the versatility and cool things that can be done with the Bitcoin protocol.

What is a Fair Shuffle?
=======================

I was faced with a problem of fairly generating a list of websites, so that no website would be given priority over the other. It is obvious if you list websites, that most users will be more attracted to, and give priority to, and read/click the links listed nearer the top compared to those in the middle and bottom. Everybody wants to be Number One, right? It is easy to shuffle any list into a random order, but the problem then faced is accusations such as “my site is never at the top!” or “my competitors site is always listed above mine!”. Basically anybody can accuse the programmer of “cooking” the shuffling of the list - cheating!

This function uses the Bitcoin Blockchain as a random seed for shuffling lists. If you present the same list in the same order as input, you are guaranteed to get the same order of output if you use
the same blockchain number/hash, on any operating system or platform.

Thus if you are running on a live website using only the last blockchain you can expect to have a
list that changes order approximately every 10 minutes which is the time a new Bitcoin blockchain is generated. This has the added benefit that you can keep lists cached for ~10 minutes so do not have to recalculate the order for every display. Thus all you need to do is display the blockchain source/number you are using for the seed generation, and tell visitors you are using this algorithm. Anybody can prove you are shuffling your lists fairly if you provide them a way of checking the original order of the list. For now I propose just leave a comment in the HTML.

An example of how to generate HTML output would be as follows:

We have the original list of ['website-a.com', 'website-b.com', 'website.c-com'] that we want to shuffle.

We retrieve the hash of the latest blockchain, in this example Bitcoin Block <a href="https://blockchain.info/block-height/295000?format=json">#295000</a> which has the associated hash: '00000000000000004d9b4ef50f0f9d686fd69db2e03af35a100370c64632a983'

We produce the following HTML:-

```html
<ul>
<!--Orig-Order: 3--><li>website-c.com</li>
<!--Orig-Order: 2--><li>website-b.com</li>
<!--Orig-Order: 1--><li>website-a.com</li>
</ul>
<p>This list generated using FairShuffle algorithm on Bitcoin Blockchain <a href="https://blockchain.info/block-height/295000">#295000</a></p>
```

Note the commented “Orig-Order”, this is so that users can verify the original order of the list which could be alphabetical, could be by added date etc... It doesn't matter, as long as they can see the original order and check that applying the FairShuffle algorithm on specified blockchain will result in the same displayed list.

Usage Ideas
===========

Can be used for lists of anything - websites, donators. Nice idea perhaps is for a election or poll, you can create
the initial list between the group and decide to fairly shuffle it based on some future blockchain.

Technical Notes
===============

It is designed for Python2 & Python3 compatability, Python3 will require random2 module as there were changes with the random functions.

I have included more testing code than program code, as I know people can be paranoid.

TODO: Make C version

TODO: Run some analysis on entire blockchain to statistically proove how faar it is.

TODO: Make HTML specific stuff, perhaps using Javascript to make some code to automatically verify list was generate fairly etc...

I don't want to add Blockchain fetching logic into this program, as I guess most using the program will already have the Blockchain or know how to get it.  Hint: https://blockchain.info/block-height/295000?format=json
