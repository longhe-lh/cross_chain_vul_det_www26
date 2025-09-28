# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Deposit1
- **rel_chain**: transfer
- **det_chain**: TokenWithdraw1
### src_chain: source_chain
- **事件**: Deposit1
  - 函数: deposit
  - 关键操作: address _account = msg.sender;, require(size==0, "bridge: only personal");, require(_account!=address(0), "bridge: zero sender");, require(msg.value==_amount, "bridge: amount");, IRC20(_token).burnFrom(_account, _amount);, IRC20(_token).transferFrom(_account, address(this), _amount);
### rel_chain: relay_chain
- **事件**: transfer
  - 函数: transfer
  - 关键操作: payable(_to).transfer(_amount);, IRC20(_token).mintTo(_to, _amount);, IRC20(_token).transfer(_to, _amount);, exists[_extra] = true;
### det_chain: destination_chain
- **事件**: TokenWithdraw1
  - 函数: withdraw
  - 关键操作: require(balanceOf[msg.sender] >= wad);, balanceOf[msg.sender] -= wad;, payable(msg.sender).transfer(wad);
---
