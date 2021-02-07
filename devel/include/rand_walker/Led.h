// Generated by gencpp from file rand_walker/Led.msg
// DO NOT EDIT!


#ifndef RAND_WALKER_MESSAGE_LED_H
#define RAND_WALKER_MESSAGE_LED_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace rand_walker
{
template <class ContainerAllocator>
struct Led_
{
  typedef Led_<ContainerAllocator> Type;

  Led_()
    : value(0)  {
    }
  Led_(const ContainerAllocator& _alloc)
    : value(0)  {
  (void)_alloc;
    }



   typedef uint8_t _value_type;
  _value_type value;



// reducing the odds to have name collisions with Windows.h 
#if defined(_WIN32) && defined(BLACK)
  #undef BLACK
#endif
#if defined(_WIN32) && defined(GREEN)
  #undef GREEN
#endif
#if defined(_WIN32) && defined(ORANGE)
  #undef ORANGE
#endif
#if defined(_WIN32) && defined(RED)
  #undef RED
#endif

  enum {
    BLACK = 0u,
    GREEN = 1u,
    ORANGE = 2u,
    RED = 3u,
  };


  typedef boost::shared_ptr< ::rand_walker::Led_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::rand_walker::Led_<ContainerAllocator> const> ConstPtr;

}; // struct Led_

typedef ::rand_walker::Led_<std::allocator<void> > Led;

typedef boost::shared_ptr< ::rand_walker::Led > LedPtr;
typedef boost::shared_ptr< ::rand_walker::Led const> LedConstPtr;

// constants requiring out of line definition

   

   

   

   



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::rand_walker::Led_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::rand_walker::Led_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::rand_walker::Led_<ContainerAllocator1> & lhs, const ::rand_walker::Led_<ContainerAllocator2> & rhs)
{
  return lhs.value == rhs.value;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::rand_walker::Led_<ContainerAllocator1> & lhs, const ::rand_walker::Led_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace rand_walker

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::rand_walker::Led_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::rand_walker::Led_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::rand_walker::Led_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::rand_walker::Led_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::rand_walker::Led_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::rand_walker::Led_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::rand_walker::Led_<ContainerAllocator> >
{
  static const char* value()
  {
    return "4391183b0cf05f8f25d04220401b9f43";
  }

  static const char* value(const ::rand_walker::Led_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x4391183b0cf05f8fULL;
  static const uint64_t static_value2 = 0x25d04220401b9f43ULL;
};

template<class ContainerAllocator>
struct DataType< ::rand_walker::Led_<ContainerAllocator> >
{
  static const char* value()
  {
    return "rand_walker/Led";
  }

  static const char* value(const ::rand_walker::Led_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::rand_walker::Led_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint8 BLACK   = 0\n"
"uint8 GREEN   = 1\n"
"uint8 ORANGE  = 2\n"
"uint8 RED     = 3\n"
"\n"
"uint8 value\n"
;
  }

  static const char* value(const ::rand_walker::Led_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::rand_walker::Led_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.value);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Led_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::rand_walker::Led_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::rand_walker::Led_<ContainerAllocator>& v)
  {
    s << indent << "value: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.value);
  }
};

} // namespace message_operations
} // namespace ros

#endif // RAND_WALKER_MESSAGE_LED_H
