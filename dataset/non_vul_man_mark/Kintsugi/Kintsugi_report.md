# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1
- **rel_chain**: mint
- **det_chain**: TokenWithdraw1
### src_chain: source_chain
- **事件**: TokenDeposit1
  - 函数: purchase
  - 关键操作: require(!_msgSender().isContract(), "cannot purchase from contract"), require(msg.value >= collections[collectionId].priceInWei, "insufficient funds sent to purchase"), require(allowedToMint, "mint not approved"), mint(collectionId, _msgSender(), recipient)
### rel_chain: relay_chain
- **事件**: mint
  - 函数: render
  - 关键操作: require(msg.sender == _owner || msg.sender == _executor, "denied"), require(args.index != -1, "rendering is finished"), require(args.index >= 0 && args.index < 64, "index must be in range 0-63"), require(args.stage >= 0 && args.stage < 104, "stage must be in range 0-103"), require(args.seed != 0, "seed not specified")
### det_chain: destination_chain
- **事件**: TokenWithdraw1
  - 函数: purchaseFor
  - 关键操作: require(!_msgSender().isContract(), "cannot purchase from contract"), require(msg.value >= collections[collectionId].priceInWei, "insufficient funds sent to purchase")
---
