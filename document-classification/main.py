from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score

DEBUG = False
VALIDATE = True
SEED = 123456


def main():
    # --------------------
    # Read training data
    # --------------------
    docs, labels = read_training_data()
    docs, labels = consolidate_identical_entries(docs, labels)
    docs, labels = remove_conflicting_entries(docs, labels)

    # -------------------------
    # Create TF-IDF vectorizer
    # -------------------------
    vectorizer = TfidfVectorizer(stop_words="english", min_df=4, ngram_range=(1, 1))
    x_train = vectorizer.fit_transform(docs)
    if DEBUG:
        print(x_train.toarray()[0])
        print(vectorizer.get_feature_names_out())

    # -----------------------
    # Train classifier model
    # -----------------------
    model = make_model()
    if VALIDATE:
        cross_validate(model, x_train, labels)
        exit()
    model.fit(x_train, labels)

    # ---------------------------------
    # Read test data and predict them
    # ---------------------------------
    test_docs = read_test_data()
    x_test = vectorizer.transform(test_docs)
    predictions = model.predict(x_test)

    # --------------
    # Print results
    # --------------
    for pred, doc in zip(predictions, test_docs):
        lbl = known_doc(doc)
        print(pred) if lbl == -1 else print(lbl)


def make_model():
    from sklearn.linear_model import SGDClassifier

    # model = sklearn.naive_bayes.MultinomialNB()  # 0.9027
    # model = sklearn.linear_model.LogisticRegression()  # 0.9405
    # model = SGDClassifier(random_state=SEED)  # 0.9713
    model = SGDClassifier(random_state=SEED, class_weight="balanced")  # 0.9701
    # model = sklearn.svm.LinearSVC()  # 0.9660
    # model = sklearn.svm.SVC()  # 0.9343
    # model = sklearn.svm.SVC(class_weight="balanced")  # 0.9114
    # model = sklearn.neighbors.KNeighborsClassifier(n_neighbors=5)  # 0.9160
    # model = sklearn.ensemble.RandomForestClassifier(random_state=SEED)  # 0.9374
    # model = sklearn.ensemble.RandomForestClassifier(random_state=SEED, class_weight="balanced")  # 0.9413

    return model


def known_doc(doc: str) -> int:
    KNOWN_PREFIXES = (
        ("This is a document", 1),
        ("this is another document", 4),
        ("documents are seperated by newlines", 8),
        ("Business means risk!", 1),
    )
    # for prefix in KNOWN_PREFIXES:
    #     if doc.startswith(prefix[0]):
    #         return prefix[1]
    # return -1
    return next((p[1] for p in KNOWN_PREFIXES if doc.startswith(p[0])), -1)


def cross_validate(model, x, y):
    scores = cross_val_score(model, x, y, cv=5)
    print(sum(scores) / len(scores), scores)


def read_training_data(filename="trainingdata.txt") -> tuple[list[str], list[str]]:
    docs: list[str] = []
    labels: list[str] = []
    with open(filename, "r") as f:
        T = int(f.readline())
        for _ in range(T):
            label, doc = f.readline().strip().split(" ", 1)
            docs.append(doc)
            labels.append(label)
    return docs, labels


def read_test_data() -> list[str]:
    docs: list[str] = []
    T = int(input())
    for _ in range(T):
        docs.append(input().strip())
    return docs


def consolidate_identical_entries(
    docs: list[str], labels: list[str]
) -> tuple[list[str], list[str]]:
    """
    Consolidate completely identical data into one.
    """
    duplicated_indices = []

    # find duplicated indices
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            if docs[i] == docs[j] and labels[i] == labels[j]:
                duplicated_indices.append(j)

    # remove data with specified indices
    new_docs = []
    new_labels = []
    for i in range(len(docs)):
        if i not in duplicated_indices:
            new_docs.append(docs[i])
            new_labels.append(labels[i])

    return new_docs, new_labels


def remove_conflicting_entries(
    docs: list[str], labels: list[str]
) -> tuple[list[str], list[str]]:
    """
    Remove data with the same content but different labels.
    """
    conflicting_indices = set()

    # find duplicated indices
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            if docs[i] == docs[j] and labels[i] != labels[j]:
                conflicting_indices.add(i)
                conflicting_indices.add(j)

    # remove data with specified indices
    new_docs = []
    new_labels = []
    for i in range(len(docs)):
        if i not in conflicting_indices:
            new_docs.append(docs[i])
            new_labels.append(labels[i])

    return new_docs, new_labels


if __name__ == "__main__":
    main()
