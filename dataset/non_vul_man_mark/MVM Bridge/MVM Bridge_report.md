# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Vault1, Bound2, Through3
- **rel_chain**: relay_event
- **det_chain**: Through1, Bound2, Vault3
### src_chain: source_chain
- **事件**: Vault1
  - 函数: receive
  - 关键操作: emit Vault(msg.sender, msg.value / BASE);
- **事件**: Bound2
  - 函数: bind
  - 关键操作: require(receiver != address(0), "invalid address");, bridges[msg.sender] = receiver;
- **事件**: Through3
  - 函数: pass
  - 关键操作: require(receiver != address(0), "no address bound");, require(amount > 0, "too small");, asset = canonical(asset);, IERC20(asset).transferFrom(msg.sender, receiver, amount);, emit Through(asset, msg.sender, receiver, amount);
### rel_chain: relay_chain
- **事件**: relay_event
  - 函数: release
  - 关键操作: require(amount > 0, "value too small");, require(bound == address(0) || receiver == bound, "bound not match");, IERC20(XIN).transferWithExtra(receiver, amount, input);
### det_chain: destination_chain
- **事件**: Through1
  - 函数: release
  - 关键操作: IERC20(XIN).transferWithExtra(receiver, amount, input);, emit Through(XIN, msg.sender, receiver, amount);
- **事件**: Bound2
  - 函数: bind
  - 关键操作: bridges[msg.sender] = receiver;, emit Bound(msg.sender, receiver);
- **事件**: Vault3
  - 函数: vault
  - 关键操作: asset = canonical(asset);, require(asset == XIN, "only XIN accepted");, IERC20(asset).transferFrom(msg.sender, address(this), amount);, emit Vault(msg.sender, amount);
---
