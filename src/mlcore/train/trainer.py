from mlcore.io.synthetic_generators import gen_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

def classification(
    X: list,
    y: list,
    random_seed: int = 42,    
) -> str:
    
    X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, stratify=y, random_state= random_seed
        )


    # scaler = StandardScaler().fit(X_train)
    # X_train_scaled = scaler.transform(X_train)

    # model = RandomForestClassifier(n_estimators=400, max_depth=None, min_samples_split=2,
    #             n_jobs=-1, random_state= random_seed).fit(X_train_scaled, y_train)


    # FOR CLASS BALANCE
    # class_weight="balanced"
    # Report additional metrics (macro F1, ROC-AUC <- predict_proba)

    model = RandomForestClassifier(n_estimators=400, n_jobs=-1, random_state= random_seed).fit(X_train, y_train)

    # X_test_scaled = scaler.transform(X_test)
    # y_pred = model.predict(X_test_scaled)
    y_pred = model.predict(X_test)

    return classification_report(y_test, y_pred)

    x, y = gen_classification(5000, 3, 3, 42)
    print(classification(x, y, 42))





