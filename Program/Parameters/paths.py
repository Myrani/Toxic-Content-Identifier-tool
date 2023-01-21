
"""
    Paths List

    RawPostsFilePath : Path to the directory where the Post scraper will dump the scraped posts
    LabeledPostFilePath : Where the User Labeled Post will be stocked
    RefinedPostsFilePath : Where the RefinedPost version of a RawPost will be stocked
    BagOfWordsFilePath : Where a Bag of words of a RefinedPost will be stocked
    ClassifiersFilePath : Where Classifiers made from bags of words will be stocked
    To modify at your own needs.
"""

paths = {"RawUserMetricsFilePath":"Results/UsersMetrics/RawUserMetrics/",
        "BaggedUserMetricsFilePath":"Results/UsersMetrics/BaggedUserMetrics/",
        "RawPostsFilePath":"Results/Posts/RawPosts/",
        "DoneRawPostsFilePath":"Results/Posts/DoneRawPosts/",
        "LabeledPostsFilePath":"Results/Posts/LabeledPosts/",
        "BagOfWordsFilePath":"Results/Posts/BagOfWords/",
        "RefinedPostsFilePath":"Results/Posts/RefinedPosts/",
        "ClassifiersFilePath":"Results/Classifiers/",
        "ParametersFileFilePath":"Program/Parameters/",
        "LabelSetsFileFilePath":"Program/Parameters/LabelSets/"}

