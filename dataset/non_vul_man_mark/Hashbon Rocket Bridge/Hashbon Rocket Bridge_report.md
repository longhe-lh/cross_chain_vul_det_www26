# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: OfferAdd1, OfferUpdate2, OrderAdd3, OrderPay4
- **rel_chain**: OrderComplete
- **det_chain**: OfferAdd1, OfferUpdate2, OrderAdd3, OrderPay4
### src_chain: source_chain
- **事件**: OfferAdd1
  - 函数: addOffer
  - 关键操作: TransferHelper.safeTransferFrom(_token, msg.sender, address(this), _amount)
- **事件**: OfferUpdate2
  - 函数: updateOffer
  - 关键操作: TransferHelper.safeTransferFrom(offers[_offerId].token, msg.sender, address(this), _amount - offers[_offerId].amount), TransferHelper.safeTransfer(offers[_offerId].token, msg.sender, offers[_offerId].amount - _amount)
- **事件**: OrderAdd3
  - 函数: addOrder
- **事件**: OrderPay4
  - 函数: payOrder
  - 关键操作: TransferHelper.safeTransferFrom(_payToken, msg.sender, _payAddress, _payAmount)
### rel_chain: relay_chain
- **事件**: OrderComplete
  - 函数: _verifySign
### det_chain: destination_chain
- **事件**: OfferAdd1
  - 函数: withdrawTokens
  - 关键操作: TransferHelper.safeTransfer(offers[offerId].token, orders[_orderId].withdrawAddress, amount), offers[offerId].amount -= amount
- **事件**: OfferUpdate2
  - 函数: withdrawTokens
  - 关键操作: TransferHelper.safeTransfer(offers[offerId].token, orders[_orderId].withdrawAddress, amount), offers[offerId].amount -= amount
- **事件**: OrderAdd3
  - 函数: withdrawTokens
  - 关键操作: TransferHelper.safeTransfer(offers[offerId].token, orders[_orderId].withdrawAddress, amount), offers[offerId].amount -= amount
- **事件**: OrderPay4
  - 函数: withdrawTokens
  - 关键操作: TransferHelper.safeTransfer(offers[offerId].token, orders[_orderId].withdrawAddress, amount), offers[offerId].amount -= amount
---
