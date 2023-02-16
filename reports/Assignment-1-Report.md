# Report

* your designs
* your answers to questions in the assignment
* your test results
* etc.

## Design
For simplicity, I did not implement my platform in any cloud, I used docker containers connected through a docker network.

The following diagram shows my intended design:

![design](design.png)

I am using the Reddit Comments dataset from Kaggle. The link provided in the description was not available,
but Kaggle published the same dataset [here.](https://www.kaggle.com/datasets/kaggle/reddit-comments-may-2015)

The dataset is a sqlite file, I used TablePlus to read the file and extract different samples to test.
The whole file is 32 GB. I uploaded a small csv sample (1000 rows) [here.](../data/small_sample_reddit_comments.csv)


### mysimbdp-coredms
For mysimbdp-coredms I used a Cassandra Cluster following what we have learnt in the tutorial. 
I chose it because it is easy to set up in a dockerized environment and offers great support for big amounts of data.

### mysimbdp-dataingest

For mysimbdp-dataingest I used RabbitMQ and created a docker container that acts as a producer, it reads data from a csv file,
selects only relevant columns and publish them to a queue called *"comments"*.

The ingestion part is done by multiple consumers (in the docker-compose file I have set a number of 4 consumers, but can be more).
When a consumer gets a message it is stored in the Cassandra database.

### mysimbdp-daas

mysimbdp-daas is a simple REST API in Flask and RabbitMQ that receives requests from clients.
* A POST request produces a message to the same queue that consumers from dataingest are using.
* A GET request asks the database for data and shows it in json format.

This part is not fully implemented since the consumers are not getting the messages.

## Answers to the Questions

### Part 1

1. * Application domain: Reddit comments; evaluate which users have more up votes to identify potential candidates for marketing purposes.
   * Data types: A single unit of data includes: text, timestamps and integers. Text for the name of the author, subreddit and content of the comment.
   Timestamp for the creation date of the comment. Integers for the number of up votes and the score of the comment.
   * Reddit is a popular platform which thousands of people use. The dataset used in this design was originally filled using the Reddit API.
   Many users are writing comments every second, resulting in a huge quantity of data to evaluate.
2. * The design and interactions of my platform are explained in the previous section.
   * I did not develop Docker, Docker Compose, Cassandra, RabbitMQ or Python for my platform. I used their official distributions.
3. Cassandra is configured as a cluster:
   * It has 2 data centers (DC1 and DC2)
   * 3 nodes: 2 nodes in DC1 and 1 node in DC2.  
   * It is using a replication factor of 3 and the simple strategy.
   * Consistency is set to Quorum.
   
   This configuration provides good consistency and availability and helps to prevent single-point-of-failure; however, there is room for improvement, for
   example having the datacenters in different machines instead of one, and having more nodes.
4. As mentioned in the previous answer, the replication level is 3, which is the same as the number of nodes, to improve it I should add 
   more nodes. The replication level should be more than one and less than the total number of nodes.
5. I would do the following: 
   * Add a RabbitMQ cluster as well, since it will help to avoid failures.
   * Have more consumers, currently I have 4 consumers, increasing to maybe 10 or more would be better.
   * Scale Cassandra horizontally by adding more nodes, and have them in different locations.

### Part 2

1. My example schema is the following:
   > comments_by_upvotes
   > - **created_utc** is a timestamp of the creation date of the comment.
   > - **ups** is an integer reflectin the number of up votes of the comment
   > - **subreddit** text, the name of the forum where the comment was posted. 
   > - **id** an alphanumerical string that identifies the comment, this is the *PRIMARY KEY*, 
   > - **author** text, the username of the person who wrote the comment 
   > - **score** int, the result of adding up votes and down votes.
   > - **body** text, the content of the comment
   
   I am using a keyspace called reddit.
2. <mark>to complete</mark>
3. * Atomic data element: reddit comment.
   * To achieve consistency I am using *quorum*, this means my data needs to be stored in the majority of
   available nodes.
4. <mark>to complete</mark>
5. * Adding more nodes to my cluster would help to increase the capacity of the database.
   * If my platform were implemented in a different environment, adding a load balancer would also help to distribute the requests more evenly.
   * Modifying my dataingest, so it uses a different and more advanced technology instead of RabbitMQ, maybe Kafka.

### Part 3

1. * **Metadata**. These are just ideas of what I could use as metadata: 
      > Name: a name for the dataset 
      > 
      > Description: a description of the data included in the dataset.
      >
      > Size: The size of the dataset
      > 
      > Owner: the tenant that created the dataset
      > 
      > Last updated: The last date in which the dataset received information.
   * **Example**: a user wants to find a dataset that contains comments on a specific subreddit. By searching the metadata 
   for the dataset, they can quickly find the dataset they need. If, for example, the name or description contain information 
   about the subreddit of each dataset, the user can search for all datasets that contain information about a subreddit, and then choose the one that best fits their 
   needs based on other metadata information, like the size, or how often the dataset is updated.
2. <mark>to complete</mark>
3. <mark>to complete</mark>
4. <mark>to complete</mark>
5. <mark>to complete</mark>