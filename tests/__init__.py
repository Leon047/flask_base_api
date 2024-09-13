import warnings

# Ignore a passlib warning
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module="passlib"
)
