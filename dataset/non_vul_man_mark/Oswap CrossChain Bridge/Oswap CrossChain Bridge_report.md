# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: NewOrder1, RequestCancelOrder2, RequestAmendOrder3
- **rel_chain**: Execute
- **det_chain**: Swap1, VoidOrder2, OrderCanceled3
### src_chain: source_chain
- **事件**: NewOrder1
  - 函数: newOrder
  - 关键操作: require(order.inAmount > 0, "input amount must be greater than zero");, order.inAmount = _transferAssetFrom(msg.sender, order.inAmount);, orderId = _newOrder(order, msg.sender);
- **事件**: RequestCancelOrder2
  - 函数: requestCancelOrder
  - 关键操作: bytes32 _orderId = hashOrder(msg.sender, sourceChainId, orderId);, require(swapOrderStatus[_orderId] == OrderStatus.NotSpecified, "BridgeVault: not a pending order");, swapOrderStatus[_orderId] = OrderStatus.RequestCancel;
- **事件**: RequestAmendOrder3
  - 函数: requestAmendOrder
  - 关键操作: require(orderOwner[orderId] == msg.sender, "BridgeVault: not from owner");, require(orderStatus[orderId] == OrderStatus.Pending || orderStatus[orderId] == OrderStatus.RequestAmend, "BridgeVault: not a pending order");, if (orderAmendments[orderId].length == 0) { orderAmendments[orderId].push(orders[orderId]); }, orderAmendments[orderId].push(order);, orderStatus[orderId] = OrderStatus.RequestAmend;
### rel_chain: relay_chain
- **事件**: Execute
  - 函数: execute
  - 关键操作: require(votingManager.isVotingContract(msg.sender), "OSWAP_VotingExecutor: Not from voting");, bytes32 hash = executeHash(params, nonce);, trollRegistry.verifySignatures(msg.sender, signatures, hash, nonce);
### det_chain: destination_chain
- **事件**: Swap1
  - 函数: swap
  - 关键操作: require(swapOrderStatus[orderId] == OrderStatus.NotSpecified,"BridgeVault: Order already processed");, require(trollRegistry.isSuperTroll(msg.sender, true), "not a super troll");, require(lastKnownBalance() >= amount, "BridgeVault: insufficient balance");, swapOrderStatus[orderId] = OrderStatus.Executed;
- **事件**: VoidOrder2
  - 函数: voidOrder
  - 关键操作: require(swapOrderStatus[orderId] == OrderStatus.NotSpecified,"BridgeVault: Order already processed");, swapOrderStatus[orderId] = OrderStatus.Cancelled;
- **事件**: OrderCanceled3
  - 函数: cancelOrder
  - 关键操作: require(orderStatus[orderId] == OrderStatus.Pending || orderStatus[orderId] == OrderStatus.RequestAmend, "BridgeVault: cancel not requested");, orderRefunds[orderId] = refundAmount;, orderStatus[orderId] = OrderStatus.RefundApproved;
---
