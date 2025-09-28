# 跨链桥合约分析报告
## 跨链桥: Safecoin
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokenDeposit1
- **rel_chain**: mint
- **det_chain**: TokenWithdraw1
### src_chain: source_chain
- **事件**: TokenDeposit1
  - 函数: mint
  - 关键操作: _mint(msg.sender, 360000 * 10 ** decimals());
### rel_chain: relay_chain
- **事件**: mint
  - 函数: mint
  - 关键操作: _mint(msg.sender, 360000 * 10 ** decimals());
### det_chain: destination_chain
- **事件**: TokenWithdraw1
  - 函数: burn
  - 关键操作: _burn(_msgSender(), amount);
---
