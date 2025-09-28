# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokenDeposit1
- **det_chain**: TokenWithdraw1
### src_chain: Fantom
- **事件**: TokenDeposit1
  - 函数: mint
  - 关键操作: require(liquidity > 0, 'UniswapV2: INSUFFICIENT_LIQUIDITY_MINTED');, _mint(to, liquidity);, _update(balance0, balance1, _reserve0, _reserve1);
### rel_chain: none
- 无事件
### det_chain: Ethereum
- **事件**: TokenWithdraw1
  - 函数: burn
  - 关键操作: require(amount0 > 0 && amount1 > 0, 'UniswapV2: INSUFFICIENT_LIQUIDITY_BURNED');, _burn(address(this), liquidity);, _safeTransfer(_token0, to, amount0);, _safeTransfer(_token1, to, amount1);
---
