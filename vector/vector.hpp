#include <memory>


template<typename _Tp, typename _Alloc>
struct VectorBase {
	typedef typename std::allocator_traits<_Alloc>::template rebind<_Tp>::other _Tp_Alloc_Type;
	typedef typename std::allocator_traits<_Tp_Alloc_Type>::pointer pointer;
	

	struct VectorData {
		pointer dataStart;
		pointer dataEnd;
		pointer storageEnd;
	
		VectorData() noexcept: dataStart(), dataEnd(), storageEnd() {}
		void CopyDataPtr(VectorData& x) noexcept {
			dataStart = x.dataStart;
			dataEnd = x.dataEnd;
			storageEnd = x.storageEnd;
		}

		void SwapData(VectorData& x) noexcept {
			VectorData temp;
			temp.CopyDataPtr(x);
			x.CopyDataPtr(*this);
			this->CopyDataPtr(temp);
		}

	};

};

template<typename _Tp, typename _Alloc=std::allocator<_Tp>>
class Vector {

private:


public:
	
	Vector() = default;
};
