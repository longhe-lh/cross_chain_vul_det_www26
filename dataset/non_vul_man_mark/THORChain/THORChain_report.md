# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Deposit1
- **rel_chain**: Outbound
- **det_chain**: TransferOut1
### src_chain: Ethereum
- **事件**: Deposit1
  - 函数: deposit
  - 关键操作: require(value > 0, "user must send assets");, iRUNE(RUNE).transferTo(address(this), value);
### rel_chain: RelayChain
- **事件**: Outbound
  - 函数: transferOut
  - 关键操作: iRUNE(RUNE).transfer(to, value);
### det_chain: THORChain
- **事件**: TransferOut1
  - 函数: transferOut
  - 关键操作: vaultAllowance[msg.sender][asset] -= amount;, asset.call(abi.encodeWithSelector(0xa9059cbb, to, amount));
---
