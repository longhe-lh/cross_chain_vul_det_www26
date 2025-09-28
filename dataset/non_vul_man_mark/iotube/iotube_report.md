# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Receipt1
- **det_chain**: OwnershipTransferred1, TokenAdded1, TokenRemoved1, Transfer1
### src_chain: source_chain
- **事件**: Receipt1
  - 函数: depositTo
  - 关键操作: require(_to != address(0), "invalid destination"), if (_token == address(0)) { require(msg.value >= _amount, "insufficient msg.value"); fee = msg.value - _amount; }, require(fee >= depositFee, "insufficient fee"), for (uint256 i = 0; i < tokenLists.length; i++) { if (tokenLists[i].isAllowed(_token)) { require(_amount >= tokenLists[i].minAmount(_token), "amount too low"); require(_amount <= tokenLists[i].maxAmount(_token), "amount too high"); } }, counts[_token] += 1;
### rel_chain: relay_chain
- 无事件
### det_chain: destination_chain
- **事件**: OwnershipTransferred1
  - 函数: transferOwnership
  - 关键操作: require(newOwner != address(0));, owner = newOwner;
- **事件**: TokenAdded1
  - 函数: addToken
  - 关键操作: if (activateItem(_token)) { require(_min > 0 && _max > _min, "invalid parameters"); }, settings[_token] = Setting(_min, _max);
- **事件**: TokenRemoved1
  - 函数: removeToken
  - 关键操作: if (deactivateItem(_token)) { emit TokenRemoved(_token); }
- **事件**: Transfer1
  - 函数: mint
  - 关键操作: (bool success, bytes memory data) = _token.call(abi.encodeWithSelector(0xa9059cbb, _to, _amount));
---
