# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: CollectionCreated1
- **rel_chain**: SendToChain
- **det_chain**: Created1
### src_chain: Ethereum
- **事件**: CollectionCreated1
  - 函数: create
  - 关键操作: require(bytes(params.name).length >= 2), _collectionsRepository.create(params, msg.sender)
### rel_chain: Avalanche
- **事件**: SendToChain
  - 函数: lzReceive
  - 关键操作: require(msg.sender == address(lzEndpoint)), require(_srcAddress.length == trustedRemote.length && trustedRemote.length > 0 && keccak256(_srcAddress) == keccak256(trustedRemote))
### det_chain: Moonbeam
- **事件**: Created1
  - 函数: omReceive
  - 关键操作: require(isOA(srcChain, srcOA)), _collectionsRepository.create(params, creator)
---
