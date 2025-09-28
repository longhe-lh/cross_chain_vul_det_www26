# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: LogSwapout1, LogAnySwapOut2
- **det_chain**: LogSwapin1, LogAnySwapIn2
### src_chain: source_chain
- **事件**: LogSwapout1
  - 函数: Swapout
  - 关键操作: _burn(_msgSender(), amount);, require(bindaddr != address(0), "bind address is the zero address");
- **事件**: LogAnySwapOut2
  - 函数: _anySwapOut
  - 关键操作: AnyswapV1ERC20(token).burn(from, amount);
### rel_chain: relay_chain
- 无事件
### det_chain: destination_chain
- **事件**: LogSwapin1
  - 函数: Swapin
  - 关键操作: _mint(account, amount);, require(newOwner != address(0), "new owner is the zero address");
- **事件**: LogAnySwapIn2
  - 函数: _anySwapIn
  - 关键操作: AnyswapV1ERC20(token).mint(to, amount);
---
