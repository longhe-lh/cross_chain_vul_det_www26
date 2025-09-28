# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: LogAnySwapOut1, LogAnySwapTradeTokensForTokens1, LogAnySwapTradeTokensForNative1
- **rel_chain**: mint, burn, depositVault, withdrawVault
- **det_chain**: LogAnySwapIn1, LogAnySwapInUnderlying1, LogAnySwapInAuto1
### src_chain: Ethereum
- **事件**: LogAnySwapOut1
  - 函数: anySwapOut
  - 关键操作: AnyswapV1ERC20(token).burn(from, amount)
- **事件**: LogAnySwapTradeTokensForTokens1
  - 函数: anySwapOutExactTokensForTokens
  - 关键操作: AnyswapV1ERC20(path[0]).burn(msg.sender, amountIn), emit LogAnySwapTradeTokensForTokens(path, msg.sender, to, amountIn, amountOutMin, cID(), toChainID)
- **事件**: LogAnySwapTradeTokensForNative1
  - 函数: anySwapOutExactTokensForNative
  - 关键操作: AnyswapV1ERC20(path[0]).burn(msg.sender, amountIn), emit LogAnySwapTradeTokensForNative(path, msg.sender, to, amountIn, amountOutMin, cID(), toChainID)
### rel_chain: RelayChain
- **事件**: mint
  - 函数: mint
  - 关键操作: _mint(to, amount), emit Transfer(address(0), account, amount)
- **事件**: burn
  - 函数: burn
  - 关键操作: _burn(from, amount), emit Transfer(account, address(0), amount)
- **事件**: depositVault
  - 函数: depositVault
  - 关键操作: _deposit(amount, to), _mint(to, amount)
- **事件**: withdrawVault
  - 函数: withdrawVault
  - 关键操作: _burn(from, amount), IERC20(underlying).safeTransfer(to, amount)
### det_chain: BinanceSmartChain
- **事件**: LogAnySwapIn1
  - 函数: anySwapIn
  - 关键操作: AnyswapV1ERC20(token).mint(to, amount), emit LogAnySwapIn(txs, token, to, amount, fromChainID, cID())
- **事件**: LogAnySwapInUnderlying1
  - 函数: anySwapInUnderlying
  - 关键操作: AnyswapV1ERC20(token).withdrawVault(to, amount, to)
- **事件**: LogAnySwapInAuto1
  - 函数: anySwapInAuto
  - 关键操作: AnyswapV1ERC20(token).mint(to, amount), emit LogAnySwapIn(txs, token, to, amount, fromChainID, cID())
---
