# TwelveData Adapter for NautilusTrader - Usage Guide

## Project Structure

```
TwelveAdapter/
├── crates/nautilus-twelvedata/     # Rust core
├── nautilus_trader/adapters/twelvedata/  # Python adapter
├── example_config.py               # Configuration examples
├── example_strategy.py             # Trading strategy example
├── main.py                         # Main entry point
├── test_final.py                   # Comprehensive tests
└── README_USAGE.md                 # This file
```

## Where Code Goes

### 1. Configuration (`example_config.py`)
**Purpose**: Set up data clients, venues, and engines  
**Location**: Separate from your strategy  
**When**: Before running backtest or live trading

```python
from example_config import create_backtest_config

config = create_backtest_config(api_key="your_key")
```

### 2. Strategy (`example_strategy.py`)
**Purpose**: Your trading logic  
**Location**: Your own strategy file  
**When**: Defines when to buy/sell

```python
from example_strategy import SimpleMovingAverageCrossStrategy

# Strategy handles on_bar(), on_start(), etc.
```

### 3. Main Script (`main.py`)
**Purpose**: Tie everything together  
**Location**: Your main entry point  
**When**: Runs the system

```python
from main import run_backtest, run_live

run_backtest(api_key="your_key")
```

### 4. Adapter Files (`nautilus_trader/adapters/twelvedata/`)
**Purpose**: Integration code (already done!)  
**Location**: In NautilusTrader installation  
**When**: Imported by your config

```python
from nautilus_trader.adapters.twelvedata import TwelveDataDataClientConfig
```

## Complete Example

### Step 1: Set API Key
```bash
export TWELVEDATA_API_KEY="your_api_key"
```

### Step 2: Create Configuration
```python
# config.py
from nautilus_trader.adapters.twelvedata import TwelveDataDataClientConfig
from nautilus_trader.config import BacktestEngineConfig

config = BacktestEngineConfig(
    data_clients=[
        TwelveDataDataClientConfig(
            api_key="your_api_key",
            default_interval="1h",
        )
    ],
)
```

### Step 3: Create Strategy
```python
# strategy.py
from nautilus_trader.strategy.strategy import Strategy

class MyStrategy(Strategy):
    def on_bar(self, bar):
        # Your trading logic here
        if bar.close > bar.open:
            self.log.info("Bullish bar")
```

### Step 4: Run
```python
# main.py
from nautilus_trader.backtest.engine import BacktestEngine

engine = BacktestEngine(config=config)
engine.add_strategy(MyStrategy, config=MyStrategyConfig())
engine.run()
```

## Quick Start (Simplest)

If you just want to **fetch data** without full NautilusTrader setup:

```python
from nautilus_twelvedata import TwelveDataHttpClientPy

client = TwelveDataHttpClientPy(api_key="your_key")
bars = client.fetch_time_series("AAPL", "1h", outputsize=100)

for bar in bars:
    print(f"{bar['datetime']}: ${bar['close']:.2f}")
```

## Full NautilusTrader Integration

For **backtesting** or **live trading** with NautilusTrader:

### 1. Configuration File
```python
# my_config.py
from nautilus_trader.adapters.twelvedata import TwelveDataDataClientConfig
from nautilus_trader.config import BacktestEngineConfig

def get_config():
    return BacktestEngineConfig(
        data_clients=[
            TwelveDataDataClientConfig(
                api_key=os.environ["TWELVEDATA_API_KEY"],
                default_interval="1h",
            )
        ],
    )
```

### 2. Strategy File
```python
# my_strategy.py
from nautilus_trader.strategy.strategy import Strategy

class MyStrategy(Strategy):
    def on_start(self):
        self.subscribe_bars(BarType.from_str("AAPL.NASDAQ.TWELVEDATA-1HR-INTERNAL"))
    
    def on_bar(self, bar):
        # Trading logic
        pass
```

### 3. Main Script
```python
# run.py
from nautilus_trader.backtest.engine import BacktestEngine
from my_config import get_config
from my_strategy import MyStrategy

config = get_config()
engine = BacktestEngine(config=config)
engine.add_strategy(MyStrategy)
engine.run()
```

## File Organization Best Practices

```
my_trading_project/
├── config/
│   ├── __init__.py
│   ├── data_config.py      # TwelveData config
│   └── venue_config.py     # Venue settings
├── strategies/
│   ├── __init__.py
│   ├── ma_cross.py         # Your strategies
│   └── mean_reversion.py
├── data/                   # Historical data (optional)
├── logs/                   # Log files
├── main.py                 # Entry point
└── requirements.txt        # Dependencies
```

## Key Points

1. **Configuration** goes in separate files from strategies
2. **Adapters** are imported in configuration, not strategies
3. **Strategies** focus on trading logic, not data fetching
4. **Main script** ties config + strategies together

## Testing Your Setup

```bash
# Test adapter
python test_final.py

# Test config
python example_config.py

# Run main
python main.py
```

## Next Steps

1. ✅ **Test the adapter** with `test_final.py`
2. 📝 **Create your strategy** in `strategies/`
3. ⚙️ **Configure your system** in `config/`
4. 🚀 **Run backtest or live trading**

The TwelveData adapter is ready to use! Just add your trading strategy.
